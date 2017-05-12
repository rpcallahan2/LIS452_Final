import readability
import csv
import nltk
import numpy
import scipy

def main():
    with open('scopus-3.csv','rb') as csvfile:
        citation_set = {}
        data_file = csv.reader(csvfile)
        for data in data_file:
            if data[1] != "Cited by" and data[3] != "[No abstract available]":
                title = data[0]
                if data[1] == "":
                    citations = 0
                else:
                    citations = eval(data[1])
                abstract = data[3]
                citation_set[title] = (citations, abstract)
    data_set = {}
    for key in citation_set:
        (citation, abstract) = citation_set[key]
        text = nltk.word_tokenize(abstract, language='english')
        try:
            read_scores = readability.getmeasures(text)
            data_dict = read_scores[u'readability grades']
            data_set[key] = (citation, data_dict[u'FleschReadingEase'])
        except UnicodeDecodeError:
            pass
    citation_scores = []
    readability_scores = []
    for key in data_set:
        (cit, read) = data_set[key]
        citation_scores.append(cit)
        readability_scores.append(read)
    x = numpy.array(readability_scores)
    y = numpy.array(citation_scores)
    stats = scipy.stats.linregress(x, y)
    print stats

main()

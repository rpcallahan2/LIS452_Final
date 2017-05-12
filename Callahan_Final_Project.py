import readability
import csv
import nltk
import numpy
import scipy

def main():
    with open('scopus-3.csv','rb') as csvfile: #open the citation and abstract data file
        citation_set = {}
        data_file = csv.reader(csvfile) #create a csv file object
        for data in data_file:
            if data[1] != "Cited by" and data[3] != "[No abstract available]": #checking to make sure it isn't the header row 
                                                                               #or a useless row
                title = data[0]
                if data[1] == "":                                              #dealing with empty citation data
                    citations = 0
                else:
                    citations = eval(data[1])                                  #converting the citations to numbers
                abstract = data[3]
                citation_set[title] = (citations, abstract)                    #creating a dictionary of titles, citations, and abstracts
    data_set = {}                                                              
    for key in citation_set:
        (citation, abstract) = citation_set[key]
        text = nltk.word_tokenize(abstract, language='english')                #prepping the abstract for analysis
        try:
            read_scores = readability.getmeasures(text)                        #analyzing the abstract
            data_dict = read_scores[u'readability grades']
            data_set[key] = (citation, data_dict[u'FleschReadingEase'])        #getting a chosen metric
        except UnicodeDecodeError:                                             #dealing with errors raised by the tokenizer and readability tool
            pass
    citation_scores = []
    readability_scores = []
    for key in data_set:
        (cit, read) = data_set[key]
        citation_scores.append(cit)                                            #creating a list of citation scores
        readability_scores.append(read)                                        #creating a list of readability scores
    x = numpy.array(readability_scores)                                        #turning the lists into arrays
    y = numpy.array(citation_scores)
    stats = scipy.stats.linregress(x, y)                                       #basic statistical analysis
    print stats

main()

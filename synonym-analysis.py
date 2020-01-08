"""
	NLP and Evolutionary Algorithm 
	==============================


	@Author: Nono Saha Cyrille Merleau(nonosaha@gmail.com)


"""

import multiprocessing as mp 
import numpy as np 
import networkx as nx 
import pandas as pd 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

import synonym 

class FilterFunction(object) : 

    def __init__(self, word):
        self.word = word
        
    def wordFilter(self, tupl) : 
        if tupl[0] == self.word: 
            return tupl


def main() : 
    """
    W0, W1 = synonym.load(synonym.PATH)
    edges = map(tuple,np.array([W0, W1]).T)
    print "Loading data done...."
    print "Starting Computating..."
    number_of_edges = np.array([len(filter(FilterFunction(word).wordFilter, edges)) for word in set(W0)])
    pd.DataFrame(np.array([list(set(W0)), number_of_edges]).T, columns=["Word","Number_of_edges"]).to_csv("Edge_number.csv")
    """ 

    data1 = pd.read_csv("Edge_number.csv")

    data2 = pd.read_csv("unigram_freq.csv")


    result = np.array([[str(elt),float(data2[data2['word']==elt]['count']), float(data1[data1['Word']==elt]['Number_of_edges'])] for elt in data1['Word'] if not data2[data2['word']==elt]['count'].empty])
    pd.DataFrame(result, columns=["word","frequence", "number_of_edges"]).to_csv('freqVSSyn.csv')
    plt.scatter(result[:,-1], result[:,1])
    plt.ylabel('Frequences')
    plt.xlabel('Number of synonyms')
    plt.title("Frequence VS Synonyms")
    plt.savefig("freqVSEdge.pdf")
    plt.show()
    #print data2[data2['word']=="fawn"]['count']

if __name__ == "__main__" : 
    main()

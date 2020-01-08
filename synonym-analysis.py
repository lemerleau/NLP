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

    W0, W1 = synonym.load(synonym.PATH)
    edges = map(tuple,np.array([W0, W1]).T)
    print "Loading data done...."
    print "Starting Computating..."
    print [len(filter(FilterFunction(word).wordFilter, edges)) for word in set(W0[:1000])]

if __name__ == "__main__" : 
    main()
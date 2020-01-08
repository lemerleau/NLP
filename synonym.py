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


PATH = "dataset_graphcomponent.csv"


def load(path) : 
    data = pd.read_csv(path)
    synomy_data = data[data['relation']=='S']
    
    W1 = synomy_data["w1"]
    W1 = np.array(W1)
    
    W0 = synomy_data["w0"]
    W0 = np.array(W0)
    
    return W0, W1

def getTriangle(sub_components): 
    
    triangles = []

    for G in sub_components:
    	A = nx.to_numpy_matrix(G)
    	if np.trace(np.linalg.matrix_power(A, 3))/6. >0 : 
		    triangles.append(G)

    return triangles	

def ifcontainstrgs(graph) : 
    A = nx.to_numpy_matrix(graph)
    if np.trace(np.linalg.matrix_power(A, 3))/6. >0 : 
        return graph
    return; 

def main() : 
    
    W0, W1 = load(PATH)
    edges = map(tuple,np.array([W0, W1]).T)
    G = nx.Graph()
    G.add_edges_from(edges[:1000])
    sub_graphs = list(nx.connected_component_subgraphs(G))
    
    print len(sub_graphs)
    pool = mp.Pool(mp.cpu_count())
    trgs= pool.map(ifcontainstrgs, sub_graphs)
    
    pool.close()
    trgs= np.array(trgs)
    trgs = trgs[trgs!=None]
    print len(sub_graphs), len(trgs)
    j = 1
    with PdfPages("Triangle.pdf") as pdf : 
        
        for g in trgs : 
            
            
            if j < 5 : 
                print j
                plt.subplot(2,2,j)
                #if len(g.nodes) < 30 : 
                nx.draw(g, with_labels = True, font_size=8, node_size=25)
                j = j+1
                
            elif j ==5 : 
                pdf.savefig()
                plt.clf()
                j = 1 

            
        plt.close()
    
if __name__=="__main__" : 
    main()

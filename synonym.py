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
from networkx.algorithms import components
#from GraphRicciCurvature.OllivierRicci import OllivierRicci


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
    nbr_of_triangles = []
    for G in sub_components:
    	A = nx.to_numpy_matrix(G)
        nb_t = np.trace(np.linalg.matrix_power(A, 3))/6.
    	if nb_t >0 : 
		    triangles.append(G)
        nbr_of_triangles.append(nb_t)
    return triangles, nbr_of_triangles

def ifcontainstrgs(graph) : 
    A = nx.to_numpy_matrix(graph)
    nb_t = np.trace(np.linalg.matrix_power(A, 3))/6.
    if nb_t >0 : 
        return graph, nb_t
    return graph, nb_t

def main() : 
    
    W0, W1 = load(PATH)
    edges = list(map(tuple,np.array([W0, W1]).T))
    G = nx.Graph()
    G.add_edges_from(edges)
    sub_graphs = list(nx.connected_component_subgraphs(G))

    test = []

    for sub in sub_graphs : 
        if len(sub.nodes) < 100 : 
            test.append(sub)
    """
    print (len(sub_graphs))
    orc = OllivierRicci(G, alpha=0.5, verbose="INFO")
    orc.compute_ricci_curvature() 

    data = [] 
    i = 0 

    print('INFO: Computation of ricci curvature done....')
    print ("Saving data....")
    for edge in edges : 

        data.append([edge[0], edge[1], orc.G[edge[0]][edge[1]]['ricciCurvature']])
        i = i +1 
        if i%1000==0 : 
            print(i*100./len(edges), "%...")

    pd.DataFrame(data, columns=['w0','w1','ricci']).to_csv("ricci.csv")
    """
    
    pool = mp.Pool(mp.cpu_count())
    trgs= pool.map(ifcontainstrgs, test[:20])
    
    pool.close()
    trgs= np.array(trgs)
    print trgs
    nb_ts = trgs[:,1]
    trgs = trgs[:,0]
    trgs = trgs[trgs!=None]
    print len(sub_graphs), len(trgs)

    print nb_ts
    j = 1
    """
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
    """
    
if __name__=="__main__" : 
    main()

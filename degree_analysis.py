import pandas as pd
import numpy as np
import RNA
import multiprocessing as mp 
import matplotlib.pyplot as plt


root_path = "Word_evol_5/100/"
df = pd.read_csv("words.csv")
dict_= list(df["word"])

def compute_degree(pop):
    
    degrees = []
    for w1 in pop : 
        neighbors = []
        for w2 in pop : 
            if RNA.hamming_distance(w1,w2) == 1 : 
                if w2 in dict_ : 
                    neighbors.append(w2)
            
        degrees.append(float(len(set(neighbors))))
    
    return degrees

def getDegree(i) : 

    dg_list = [0]
    for file_ in os.listdir(root_path+str(i)) : 
        df = pd.read_csv(root_path+ str(i)+"/"+file_)
        dg_list.append(np.mean(compute_degree(dict_, df.get_values()[:,1])))
    return dg_list

def main() : 

    pool = mp.Pool(mp.cpu_count())
    degree_data = pool.map(getDegree, range(5))
    pool.close()

    for degrees in degree_data: 
        plt.plot(degrees)
    
    plt.xlabel('generation')
    plt.ylabel(r'Mean Neutral degree $<d>$')
    plt.title(r"$\mu =10/N, N=100, t=10^3, runs=100$")
    plt.savefig(root_path+"mean_degree10run.pdf")
    plt.show()

        

if __name__ == "__main__" : 
    main()
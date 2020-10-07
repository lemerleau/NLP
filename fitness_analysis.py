import pandas as pd
import numpy 
import multiprocessing as mp 
import os 


df = pd.read_csv("words.csv")
dict_= list(df["word"])

root_path = "Word_evol_5/100/"

def compute_fitnesses(dict_, pop) : 
    fitnesses = [] 
    for word in pop : 
        if word in dict_ : 
            fitnesses.append(1.)
        else : 
            fitnesses.append(0.)
    
    return fitnesses

def getFitnesses(i): 
      
    fitness_run = [1.]
    for file_ in os.listdir(root_path+str(i)) : 
        df = pd.read_csv(root_path+ str(i)+"/"+file_)
        fitness_run.append(np.median(compute_fitnesses(dict_,df.get_values()[:,1])))
    return fitness_run


def main() : 

    pool = mp.Pool(mp.cpu_count())
    fit_data= pool.map(getFitnesses, range(100))
    pool.close()

    for fit in fit_data: 
        plt.plot(fit)
    plt.xlabel('generation')
    plt.ylabel(r'Mean fitness')
    plt.title(r"$\mu =0.1, N=1000, t=10^3, runs=100$")
    plt.savefig(root_path+"mean_fitness100run.pdf")
    plt.show()


if __name__=="__main__" : 
    main()

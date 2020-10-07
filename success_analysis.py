import pandas as pd
import numpy 
import multiprocessing as mp 
import os 


df_word = pd.read_csv("words.csv")
dict_= list(df_word["word"])

root_path = "Word_evol_5/"


def main() : 

    successes = []
    gen_data = []
    n_s = [100, 500, 1000] 
    for i in n_s: 
        gens = []
        for j in range(100) : 
            
            gens.append(len(os.listdir(root_path+str(i)+"/"+str(j))))
        gen_data.append(gens)
        gens = np.array(gens) 
        successes.append(len(gens[gens<1000]))
    print successes

    success = np.array(success)
    plt.plot(n_s, successes, 'r-o')
    plt.xlabel('Pop Size(N)')
    plt.ylabel("Number of success")
    plt.title(r'$mu = 10/N, t_{max}=10^3$')
    plt.savefig(root_path+"success.pdf")

    plt.show()

    df_gen = pd.DataFrame(np.array(gen_data).T, columns=n_s)
    boxplot = df_gen.boxplot(column=n_s)
    plt.xlabel('Pop Size(N)')
    plt.ylabel("Number of success")
    plt.title(r'$mu = 10/N, t_{max}=10^3$')
    plt.savefig("box_plot.pdf")

    plt.show()


if __name__ == "__main__" : 

    main()

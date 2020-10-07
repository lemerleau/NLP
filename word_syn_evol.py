import numpy 
import RNA 
import string 
import pandas
import pp
import synonym 
import os
import networkx as nx


def mutate(G, pt, mu) : 
    indexes_tomutate = list(numpy.where(numpy.random.binomial(2,mu, len(pt))==1)[0])
    
    for i in indexes_tomutate: 
        v_w = numpy.array(list(G.edges(pt[i])))
        try:
            v_w = v_w[:,1]
        except IndexError : 
            print v_w, G.edges(pt[i]), pt[i]

        pt[i] = numpy.random.choice(v_w, 1)[0]
    return pt
        

def select(pt_prime, size) :     
    return numpy.random.choice(pt_prime, size)


def word_evol(G,init_pop, t, n , mu ) : 

    timer = 0 
    prev_pop = list(numpy.copy(init_pop))

    try : 
        os.makedirs(os.getcwd()+"/logs/simul1/")
    except OSError : 
        pass

    while timer<t : 
        
        if timer%100 == 0 : 
            print "Generation = ", timer
        mutated_pop = mutate(G,prev_pop, mu)
        new_pop = select(mutated_pop, n)

        pandas.DataFrame(new_pop).to_csv("logs/simul1/gen"+str(timer)+".csv")

        prev_pop = list(numpy.copy(new_pop))

        timer +=1 

    
    return timer, prev_pop



def main() : 
    n=1000
    mu = 0.4
    t = 10000
    nbjobs = 10

    df_edge = pandas.read_csv("edge_giant.csv")
    edges_giant = []
    for line_ in df_edge.get_values(): 
        edges_giant.append((line_[1],line_[2]))
    
    G_freq = nx.Graph(directed=False)

    G_freq.add_edges_from(edges_giant)
    init_pop = list(numpy.random.choice(["deferment"], n))

    print "=================Init pop================================"
    print init_pop
    print "----------------------------------------------------------"

    print "=================Last pop================================"
    result = word_evol(G_freq, init_pop, t, n, mu)





    """
    #tuple of all parallel python servers to connect with
    ppservers = ()
    job_server = pp.Server(nbjobs, ppservers=ppservers)
    
    tasks = range(nbjobs)
    result = []
    
    print "Start running jog"
    jobs = [(task, job_server.submit(word_evol, (meaningful_w, generation, n, mu,), ( mutate, select,),
                                            ("numpy", "RNA","pandas", "string"))) for task in tasks]
    
    for task, job in jobs : 
        gen = job()
        result.append(gen[0])


    #SAVED CODE FOR EDGE DATA PRODUCTION
    W0, W1 = synonym.load(synonym.PATH)
    edges = map(tuple,numpy.array([W0, W1]).T)

    G = nx.Graph()
    G.add_edges_from(edges)
    

    
    df_freq = pandas.read_csv("freqVSSyn.csv")
    df_freq

    reduced_edges = []
    for list_ in df_freq.get_values(): 
        all_edges = numpy.array(list(G.edges(list_[1])))
        reduced_edges.append([edge for edge in all_edges if edge[1] in list(df_freq["word"])])
    merged_edges = sum(reduced_edges,[])
    print(len(merged_edges))

    G_freq = nx.Graph()
    G_freq.add_edges_from(merged_edges)

    for g in list(nx.connected_component_subgraphs(G_freq)) : 
        if len(g.nodes) == 15287 : 
            print "Number of nodes of the giant component is, ", len(g.nodes) 
            G_giant = g

    G_giant_edges = list(G_giant.edges) 

    pandas.DataFrame(G_giant_edges).to_csv("edge_giant.csv")

    """
    print "End of jobs"

    print result


if __name__=="__main__" : 

    main()






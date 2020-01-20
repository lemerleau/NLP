import numpy 
import RNA 
import string 
import pandas
import pp



def mutate(pop,mu) :  

        alphabat = list(string.ascii_lowercase)

        mutated_pop = []
        for word in pop: 
            r = numpy.random.rand(4)
            w = numpy.array(list(word))
            mut_pos =w[r<mu] 
            choices = numpy.random.choice(alphabat, len(mut_pos))
            w[r<mu] = choices
            
            mutated_pop.append("".join(w))
       
        return mutated_pop

def select(dict_, pop, size) : 
    
    fitnesses = [] 
    for word in pop : 
        if word in dict_ : 
            fitnesses.append(1.)
        else : 
            fitnesses.append(0.)
    
    fitnesses = numpy.array(fitnesses)
    
    return numpy.random.choice(pop, size, p=fitnesses/sum(fitnesses))


def word_evol(dict_, generation, n , mu ) : 

    timer = 0 
    init_pop = numpy.random.choice(['opus'], size =n)
    prev_pop = numpy.copy(init_pop)

    while timer<generation and "arts" not in prev_pop : 
        
        if timer%100 == 0 : 
            print "Generation = ", timer
        mutated_pop = mutate(prev_pop, mu)
        new_pop = select(dict_ ,mutated_pop, n)

        prev_pop = numpy.copy(new_pop)

        timer +=1 

    
    return timer, prev_pop



def main() : 
    n=100
    mu = 0.1
    
    
    generation = 100
    df = pandas.read_csv("words.csv")
    meaningful_w = list(df["word"]) 
    nbjobs = 2
    
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
    
    print "End of jobs"

    print result


if __name__=="__main__" : 

    main()






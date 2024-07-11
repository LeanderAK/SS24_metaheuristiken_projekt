#Create function to mutate a single route
#we’ll use swap mutation.
#This means that, with specified low probability, 
#two cities will swap places in our route.
import random


def mutate(individual, mutationRate):
    for swapped in range(len(individual)):
        if(random.random() < mutationRate):
            swapWith = int(random.random() * len(individual))
            
            city1 = individual[swapped]
            city2 = individual[swapWith]
            
            individual[swapped] = city2
            individual[swapWith] = city1
    return individual


#Create function to run mutation over entire population
def mutatePopulation(population, mutationRate, eliteSize):
    mutatedPop = []
    
    #mating pool is sorted in order of fitness
    #here elitism instead of fixed archive
    #TODO: ein festes Archiv vorsehen wie es im ursprünglichen SPEA2 vorgesehen ist 
    for ind in range(0, eliteSize):
        mutatedPop.append(population[ind])
    for ind in range(eliteSize, len(population)):
    #for ind in range(0, len(population)):
        mutatedInd = mutate(population[ind], mutationRate)
        mutatedPop.append(mutatedInd)
    return mutatedPop
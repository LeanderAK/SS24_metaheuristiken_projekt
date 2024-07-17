import random
from .fitness import Fitness

#Create mating pool
def get_individuals_by_indices(population, selectionResults):
    pool = []
    for i in range(0, len(selectionResults)):
        index = selectionResults[i]
        pool.append(population[index])
    return pool

# Create a crossover function for two parents to create one child
def breed(parent1, parent2):
    child = []
    childP1 = []
    childP2 = []
    
    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent1))
    
    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    #In ordered crossover, we randomly select a subset of the first parent string
    for i in range(startGene, endGene):
        childP1.append(parent1[i])

    #and then fill the remainder of the route with the genes from the second parent
    #in the order in which they appear, 
    #without duplicating any genes in the selected subset from the first parent      
    childP2 = [item for item in parent2 if item not in childP1]

    child = childP1 + childP2
    return child


#Create function to run crossover over full mating pool
def breedPopulation(matingpool):
    children = []
    pool = random.sample(matingpool, len(matingpool))

    #we use the breed function to fill out the rest of the next generation.    
    for i in range(0, len(matingpool)):
        child = breed(pool[i], pool[len(matingpool)-i-1])
        children.append(child)
    return children



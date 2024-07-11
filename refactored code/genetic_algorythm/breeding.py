import random
from .route import Route

def matingPool(population: list[Route], selectionResults) -> list[Route]:
    matingpool:list[Route] = []
    for i in range(0, len(selectionResults)):
        index = selectionResults[i]
        matingpool.append(population[index])
    return matingpool

# Create a crossover function for two parents to create one child
def breed(parent1:Route, parent2:Route) -> Route:
    child = []
    childP1 = []
    childP2 = []
    
    geneA = int(random.random() * parent1.number_of_cities())
    geneB = int(random.random() * parent1.number_of_cities())
    
    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    #In ordered crossover, we randomly select a subset of the first parent string
    for i in range(startGene, endGene):
        childP1.append(parent1.get_cities()[i])

    #and then fill the remainder of the route with the genes from the second parent
    #in the order in which they appear, 
    #without duplicating any genes in the selected subset from the first parent      
    childP2 = [item for item in parent2.get_cities() if item not in childP1]

    child = childP1 + childP2
    return Route(child)

#Create function to run crossover over full mating pool
def breedPopulation(matingpool: list[Route], eliteSize) -> list[Route]:
    children = []
    length = len(matingpool) - eliteSize
    pool = random.sample(matingpool, len(matingpool))

    #we use elitism to retain the best routes from the current population.
    for i in range(0,eliteSize):
        children.append(matingpool[i])

    #we use the breed function to fill out the rest of the next generation.    
    for i in range(0, length):
        child = breed(pool[i], pool[len(matingpool)-i-1])
        children.append(child)
    
    return children

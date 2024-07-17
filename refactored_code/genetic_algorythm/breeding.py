import random
from .fitness import Fitness
from .city import City

#Create mating pool
def get_individuals_by_indices(population: list[list[City]], selectionResults: list[int]) -> list[list[City]]:
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
def breedPopulation(matingpool:list[list[City]], target_children_amount:int):
    """_summary_

    Args:
        matingpool (list[list[City]]): the selected individuals that are going to breed
        target_children_amount (int): how many children do we need?

    Returns:
        _type_: _description_
    """
    # for now we just go through the mating list over and over and select randomly from those -> this can be adjusted
    # we dont have partners for life producing multiple children, our algoythm goes against marriage xD
    children:list[list[City]] = []

    #we use the breed function to fill out the rest of the next generation.    
    while len(children) < target_children_amount: 
        temp_mating_pool = matingpool.copy()
        
        while(len(temp_mating_pool) > 2):
            partners = random.sample(temp_mating_pool,2)
            temp_mating_pool.remove(partners[0])
            temp_mating_pool.remove(partners[1])
            children.append(breed(partners[0],partners[1]))
            
            if(len(children) == target_children_amount):
                break
    

    return children



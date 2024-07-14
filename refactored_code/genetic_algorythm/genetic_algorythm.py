from .fitness import Fitness
from .city import City
from .other_helper_functions import *
from .ranking import *
from .selection import *
from .breeding import *
from .mutation import *
from .plot_helpers import *
from .initial_population import *
import numpy as np, random, operator, pandas as pd, matplotlib.pyplot as plt

#Put all steps together to create the next generation
 
#First, we rank the routes in the current generation using rankRoutes.
#We then determine our potential parents by running the selection function,
#    which allows us to create the mating pool using the matingPool function.
#Finally, we then create our new generation using the breedPopulation function 
# and then applying mutation using the mutatePopulation function. 

def nextGeneration(currentGen, eliteSize, mutationRate, objectiveNrUsed, archiveUsed) -> list[list[City]]: 
   # rankRoutesBasedOnDominance(currentGen)
    #print("\n\n pop pre ranked",currentGen)
    popRanked = rankRoutes(currentGen,objectiveNrUsed)
    #print("\n\n pop ranked",popRanked)
    if (not archiveUsed):
        selectionResults = selection(popRanked, eliteSize)
        
        matingpool = matingPool(currentGen, selectionResults)
        #print("\n\n next selectionResults",matingpool)
        children = breedPopulation(matingpool, eliteSize)
        #print("\n\n next children",children)
        nextGeneration = mutatePopulation(children, mutationRate,0)
    else:
        #<<<<< use archiv
        #TODO: ein festes Archiv vorsehen wie es im ursprünglichen SPEA2 vorgesehen ist 
        selectionResults = selectionWithArchive(popRanked)
        matingpool = matingPool(currentGen, selectionResults)
        archiveSize = determineNonDominatedArchiveSize(popRanked)
        children = breedPopulation(matingpool, archiveSize)
        
        
        #eliteSize is used to maintain solutions that should be in an archive
        nextGeneration = mutatePopulation(children, mutationRate, eliteSize)
    
    return nextGeneration


def geneticAlgorithm(objectiveNrUsed, population_genes, popSize, eliteSize, mutationRate, generations):
    #create initial population
    population = initialPopulation(popSize, population_genes)
    
    archiveUsed = False
    
    #provide statistics about best initial solution with regard to chosen objective
    if (objectiveNrUsed == 1 or objectiveNrUsed == 2):
        print("Initial objective: " + str(1 / rankRoutes(population,objectiveNrUsed)[0][1]))
        bestRouteIndex = rankRoutes(population,objectiveNrUsed)[0][0]
        bestRoute = population[bestRouteIndex]
        print("Initial distance : " + str(Fitness(bestRoute).routeDistance()))
        print("Initial stress:    " + str(Fitness(bestRoute).routeStress()))
        plotRoute(bestRoute, "Best initial route")
    elif(objectiveNrUsed == 3):
        print("Initial highest fitness value: " + str(rankRoutes(population,objectiveNrUsed)[0][1]))
        print("Initial best distance value: " + str(1/ rankRoutes(population,1)[0][1]))
        print("Initial best stress value: " + str(1/ rankRoutes(population,2)[0][1]))
        archiveUsed = True
    
    #plot intial population with regard to the two objectives
    plotPopulationAndObjectiveValues(population, "Initial Population")
    
    #store infos to plot progress when finished
    progressDistance = []
    progressDistance.append(1 / rankRoutes(population,1)[0][1])
    progressStress = []
    progressStress.append(1 / rankRoutes(population,2)[0][1])
    
    
    #create new generations of populations
    for i in range(0, generations):
        if(i%10 == 0):
            print(f'\r... computing - generation: {i + 1}/{generations}', end='')
        #print(i, end=", ")
        population = nextGeneration(population, eliteSize, mutationRate,objectiveNrUsed,archiveUsed)
        #store infos to plot progress when finished
        progressDistance.append(1 / rankRoutes(population,1)[0][1])
        progressStress.append(1 / rankRoutes(population,2)[0][1])
    print("\n Done!")
        
    #plot progress - distance
    plt.plot(progressDistance)
    plt.ylabel('Distance')
    plt.xlabel('Generation')
    plt.title('Progress of Distance Minimization')
    plt.show()
    #plot progress - stress
    plt.plot(progressStress)
    plt.ylabel('Stress')
    plt.xlabel('Generation')
    plt.title('Progress of Stress Minimization')
    plt.show()
    
    #provide statistics about best final solution with regard to chosen objective
    if (objectiveNrUsed == 1 or objectiveNrUsed == 2):
        print("Final objective: " + str(1 / rankRoutes(population,objectiveNrUsed)[0][1])) 
        bestRouteIndex = rankRoutes(population,objectiveNrUsed)[0][0]
        bestRoute = population[bestRouteIndex]
        print("Final distance : " + str(Fitness(bestRoute).routeDistance()))
        print("Final stress:    " + str(Fitness(bestRoute).routeStress()))
        
        #Provide special initial solutions    <<<<<<<<<<<
        #print city Indizes for initial solution
        bestRouteIndices = []
        for city in bestRoute:
            bestRouteIndices.append(city.nr)
    
        print("---- ")
        print("City Numbers of Best Route")
        print(bestRouteIndices)
        print("---- ")
        plotRoute(bestRoute, "Best final route")
        
    elif(objectiveNrUsed == 3):
        print("Final highest fitness value: " + str(rankRoutes(population,objectiveNrUsed)[0][1]))
        print("Final best distance value: " + str(1/ rankRoutes(population,1)[0][1]))
        print("Final best stress value: " + str(1/ rankRoutes(population,2)[0][1]))
        bestRouteIndex = rankRoutes(population,objectiveNrUsed)[0][0]
        bestRoute = population[bestRouteIndex]
        #TODO: ein festes Archiv vorsehen wie es im ursprünglichen SPEA2 vorgesehen ist
        # dann alle Lösungen ausgeben die im Archiv sind
        
        
    #plot final population with regard to the two objectives
    plotPopulationAndObjectiveValues(population, "Final Population")
    

    
    return bestRoute
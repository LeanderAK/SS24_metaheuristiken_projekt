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

def nextGeneration(objectiveNrUsed, selectionNrUsed, currentGen, eliteSize, breeding_rate, mutationRate, archiveUsed, archive = None, archiveSize= None) -> list[list[City]]: 
   # rankRoutesBasedOnDominance(currentGen)
    #print("\n\n pop pre ranked",currentGen)
    #print("\n\n pop ranked",popRanked)
    if (not archiveUsed):
        popRanked = rankRoutes(currentGen,objectiveNrUsed)
        mating_condidates_indices, elites_indices = select_mating_candidates_and_elites(selectionNrUsed, popRanked, eliteSize, breeding_rate)
        
        matingpool:list[list[City]] = get_individuals_by_indices(currentGen, mating_condidates_indices)
        elites:list[list[City]] = get_individuals_by_indices(currentGen, elites_indices)
        #print("\n\n next selectionResults",matingpool)
        children:list[list[City]] = breedPopulation(matingpool, len(currentGen)-eliteSize)
        #print("\n\n next children",children)
        nextGeneration:list[list[City]] = elites + mutatePopulation(children, mutationRate,0) 
        #print("next generation size: ", len(nextGeneration))
        return nextGeneration, None
    else:
        #<<<<< use archiv
        currentGenAndArchive = currentGen + archive
        currentGenAndArchiveFitness = rankRoutes(currentGenAndArchive, objectiveNrUsed)

        mating_candidates_indices, elites_indices = select_mating_candidates_and_elites(selectionNrUsed=selectionNrUsed, popRanked=currentGenAndArchiveFitness, eliteSize=eliteSize,breeding_rate=breeding_rate)
        matingpool = get_individuals_by_indices(currentGenAndArchive, mating_candidates_indices)
        # archiveSize = determineNonDominatedArchiveSize(popRanked)
        children = breedPopulation(matingpool, len(currentGen)-eliteSize)
        
        elites:list[list[City]] = get_individuals_by_indices(currentGenAndArchive, elites_indices)
        #eliteSize is used to maintain solutions that should be in an archive
        nextGeneration = elites + mutatePopulation(children, mutationRate, 0)

        nextArchive = createNextArchive(population=currentGenAndArchive,rankedPopulation=currentGenAndArchiveFitness,archiveSize=archiveSize)
        

        return nextGeneration, nextArchive
    


def geneticAlgorithm(objectiveNrUsed, initialPopNrUsed, selectionNrUsed, population_genes, popSize, eliteSize, breeding_rate, mutationRate, generations, archiveSize= None):
    #create initial population
    population = initialPopulation(initialPopNrUsed, popSize, population_genes)
    
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
    archive = []
    for i in range(0, generations):
        if(i%10 == 0):
            print(f'\r... computing - generation: {i + 1}/{generations}', end='')
        #print(i, end=", ")
        population, archive = nextGeneration(
            objectiveNrUsed=objectiveNrUsed,
            selectionNrUsed=selectionNrUsed, 
            currentGen=population, 
            eliteSize=eliteSize,
            breeding_rate=breeding_rate, 
            mutationRate=mutationRate, 
            archiveUsed=archiveUsed,
            archive=archive,
            archiveSize=archiveSize
        )
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
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

def nextGeneration(objectiveNrUsed, selectionNrUsed, currentGen, eliteSize, breeding_rate, mutationRate, archiveUsed, archive = None, archiveSize= None) -> tuple[list[list[City]],list[list[City]]]: 
    """
    return a touple of 
    [0] next generation
    [1] next archive
    """
   # rankRoutesBasedOnDominance(currentGen)
    #print("\n\n pop pre ranked",currentGen)
    #print("\n\n pop ranked",popRanked)
    if (not archiveUsed):
        popRanked:list[tuple[int,float]] = rankRoutes(currentGen,objectiveNrUsed)
        #print("pop ranked first", Fitness(getCityBasedOnNr(currentGen,popRanked[0][0])).routeDistance())
        mating_condidates_indices:list[int] = select_mating_candidates(selectionNrUsed, popRanked, eliteSize, breeding_rate)
        elites_indices:list[int] = get_elites_indices(popRanked=popRanked,eliteSize=eliteSize)
        
        matingpool:list[list[City]] = get_individuals_by_indices(currentGen, mating_condidates_indices)
        elites:list[list[City]] = get_individuals_by_indices(currentGen, elites_indices)
        
        #print("\n\n next selectionResults",matingpool)
        children:list[list[City]] = breedPopulation(matingpool, len(currentGen)-eliteSize)
        #print("\n\n next children",children)
        nextGeneration:list[list[City]] = elites + mutatePopulation(children, mutationRate) 
        #print("elites  size: ", len(elites))
        #print("elites  first: ", Fitness(elites[0]).routeDistance())
        #print("next generation size: ", len(nextGeneration))
        return nextGeneration, []
    else:
      
        currentGenAndArchive = currentGen + archive
        currentGenAndArchiveRanked:list[tuple[int,float]] = rankRoutes(currentGenAndArchive, objectiveNrUsed)

        mating_candidates_indices:list[int] = select_mating_candidates(selectionNrUsed=selectionNrUsed, popRanked=currentGenAndArchiveRanked, eliteSize=eliteSize,breeding_rate=breeding_rate)
        elites_indices:list[int] = get_elites_indices(popRanked=currentGenAndArchiveRanked,eliteSize=eliteSize)

        matingpool:list[list[City]] = get_individuals_by_indices(currentGenAndArchive, mating_candidates_indices)
        elites:list[list[City]] = get_individuals_by_indices(currentGenAndArchive, elites_indices)
        
        # archiveSize = determineNonDominatedArchiveSize(popRanked)
        
        children:list[list[City]] = breedPopulation(matingpool, len(currentGen)-eliteSize)
        
        #eliteSize is used to maintain solutions that should be in an archive
        nextGeneration:list[list[City]] = elites + mutatePopulation(children, mutationRate)
        nextArchive = createNextArchive(population=currentGenAndArchive,rankedPopulation=currentGenAndArchiveRanked,archiveSize=archiveSize)
        
        return nextGeneration, nextArchive
    


def geneticAlgorithm(
        objectiveNrUsed, initialPopNrUsed, selectionNrUsed, 
        population_genes, popSize, eliteSize, breeding_rate,
        mutationRate, generations, archiveUsed=False, 
        archiveSize=20, plot_level=0
    ):
    assert (eliteSize < (popSize*0.5)), "keep the elite size under 50% of the total population"
    assert (breeding_rate > 0.001 and breeding_rate < 0.51), "keep the breeding rate between 0.01 and 0.5"

    
    #create initial population
    population = initialPopulation(initialPopNrUsed, popSize, population_genes)
    
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
    
    #plot intial population with regard to the two objectives
    if plot_level > 1:
        plotPopulationAndObjectiveValues(population, "Initial Population")
    
    #store infos to plot progress when finished
    progressDistance:list[float] = []
    progressStress:list[float] = []
    progressHyperVolume:list[float] = []
    
    progressDistance.append(1 / rankRoutes(population,1)[0][1])
    progressStress.append(1 / rankRoutes(population,2)[0][1])
    
    
    #create new generations of populations
    archive = []
    for i in range(0, generations):
        if(i%10 == 0):
            print(f'\r... computing - generation: {i + 1}/{generations}', end='')
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
        if(objectiveNrUsed == 3 and len(archive) > 0):
            progressHyperVolume.append(get_hypervolume_value(archive))

        
        if plot_level > 2:
            plotPopulationAndObjectiveValues(population, f"Generation: {i+1}",archive)

    print("\n Done!")
        
    if plot_level > 1:
        plotProgress(progressDistance,'Distance')
        plotProgress(progressStress,'Stress')
        if(objectiveNrUsed == 3 and len(archive) > 0):
            plotProgress(progressHyperVolume,'Hypervolume')

    
    #provide statistics about best final solution with regard to chosen objective
    if (objectiveNrUsed == 1 or objectiveNrUsed == 2):
        print("Final objective: " + str(1 / rankRoutes(population,objectiveNrUsed)[0][1])) 
        bestRouteIndex = rankRoutes(population,objectiveNrUsed)[0][0]
        bestRoute = population[bestRouteIndex]
        print("Final distance : " + str(Fitness(bestRoute).routeDistance()))
        print("Final stress:    " + str(Fitness(bestRoute).routeStress()))
        
        #print city Indizes for initial solution
        bestRouteIndices = []
        for city in bestRoute:
            bestRouteIndices.append(city.nr)
    
        print("---- ")
        print("City Numbers of Best Route")
        print(bestRouteIndices)
        print("---- ")
        if plot_level > 0:
            plotRoute(bestRoute, "Best final route")
        
    elif(objectiveNrUsed == 3):
        print("Final highest fitness value: " + str(rankRoutes(population,objectiveNrUsed)[0][1]))
        print("Final best distance value: " + str(1/ rankRoutes(population,1)[0][1]))
        print("Final best stress value: " + str(1/ rankRoutes(population,2)[0][1]))
        if( len(archive) > 0):
            hypervolume_value = get_hypervolume_value(archive)
            print("final hypervolume value: ", reformat_hypervolume_value(hypervolume_value))
        
        
        bestRouteIndex = rankRoutes(population,objectiveNrUsed)[0][0]
        bestRouteFitness = rankRoutes(population,objectiveNrUsed)[0][1]
        bestRoute = population[bestRouteIndex]
        #TODO: ein festes Archiv vorsehen wie es im ursprünglichen SPEA2 vorgesehen ist
        # dann alle Lösungen ausgeben die im Archiv sind

        
        if plot_level > 0:
            plotPopulationAndObjectiveValues(population, "Final Population",archive)
            if( len(archive) > 0):
                plot_hypervolume(archive)
        
        return bestRoute, bestRouteFitness
    #plot final population with regard to the two objectives
    
    
    return bestRoute, None
from .route import Route
from .city import City
from .other_helper_functions import *
from .plot_helpers import *
from .initial_population import initialPopulation
import numpy as np, random, operator, pandas as pd, matplotlib.pyplot as plt


def geneticAlgorithm(objectiveNrUsed, specialInitialSolutions: list[Route], population_genes, popSize, eliteSize, mutationRate, generations):
    """_summary_

    Args:
        objectiveNrUsed (_type_): _description_
        specialInitialSolutions (list[Route]): _description_
        population_genes (_type_): can be seen as the genes that are going to get switched up, in our case, its the cities
        popSize (_type_): _description_
        eliteSize (_type_): _description_
        mutationRate (_type_): _description_
        generations (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    #create initial population
    population:list[Route] = initialPopulation(popSize, population_genes, specialInitialSolutions)
    
    archiveUsed = False
    
    #print("initial population: ", pop)
    ranked_routes_indices:list[tuple[int,float]] = rankRoutes(population,objectiveNrUsed)
    print("ranked routes indices: ", ranked_routes_indices[0][0])
    bestRoute:Route = population[ranked_routes_indices[0][0]]
    print("best Route: ", bestRoute)
    assert isinstance(bestRoute,Route)
    
    bestRouteFitness:float = ranked_routes_indices[0][1]

    #provide statistics about best initial solution with regard to chosen objective
    if (objectiveNrUsed == 1 or objectiveNrUsed == 2):          
        print("Initial objective: " + str(1 / bestRouteFitness))
        print("Initial distance : " + str(bestRoute.routeDistance()))
        print("Initial stress:    " + str(bestRoute.routeStress()))        
    elif(objectiveNrUsed == 3):
        print("Initial highest fitness value: " + str(rankRoutes(population,objectiveNrUsed)[0][1]))
        print("Initial best distance value: " + str(1/ rankRoutes(population,1)[0][1]))
        print("Initial best stress value: " + str(1/ rankRoutes(population,2)[0][1]))
        archiveUsed = True
    
    plotRoute(bestRoute, "Best initial route")
    #plot intial population with regard to the two objectives
    plotPopulationAndObjectiveValues(population, "Initial Population")
    
    #store infos to plot progress when finished
    progressDistance = []
    progressDistance.append(1 / rankRoutes(population,1)[0][1])
    progressStress = []
    progressStress.append(1 / rankRoutes(population,2)[0][1])
    
    
    #create new generations of populations
    for i in range(0, generations):
        print(i, end=", ")
        population = nextGeneration(population, eliteSize, mutationRate,objectiveNrUsed,archiveUsed)
        #store infos to plot progress when finished
        progressDistance.append(1 / rankRoutes(population,1)[0][1])
        progressStress.append(1 / rankRoutes(population,2)[0][1])
    print("Done!")
        
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
    
    bestFinalRoute:Route = population[rankRoutes(population,objectiveNrUsed)[0][0]]
    
    #provide statistics about best final solution with regard to chosen objective
    if (objectiveNrUsed == 1 or objectiveNrUsed == 2):
        print("Final objective: " + str(1 / rankRoutes(population,objectiveNrUsed)[0][1])) 
        #bestRouteIndex = rankRoutes(pop,objectiveNrUsed)[0][0]
        
        print("Final distance : " + str(bestFinalRoute.routeDistance()))
        print("Final stress:    " + str(bestFinalRoute.routeStress()))
        
        #Provide special initial solutions    <<<<<<<<<<<
        #print city Indizes for initial solution
        bestRouteIndizes = []
        for city in bestFinalRoute.get_cities():
            bestRouteIndizes.append(city.nr)
    
        print("---- ")
        print("City Numbers of Best Route")
        print(bestRouteIndizes)
        print("---- ")
        plotRoute(bestFinalRoute, "Best final route")
        
    elif(objectiveNrUsed == 3):
        print("Final highest fitness value: " + str(rankRoutes(population,objectiveNrUsed)[0][1]))
        print("Final best distance value: " + str(1/ rankRoutes(population,1)[0][1]))
        print("Final best stress value: " + str(1/ rankRoutes(population,2)[0][1]))
        #bestRouteIndex = rankRoutes(pop,objectiveNrUsed)[0][0]
        #bestRouteTuple = pop[bestRouteIndex]
        #TODO: ein festes Archiv vorsehen wie es im ursprünglichen SPEA2 vorgesehen ist
        # dann alle Lösungen ausgeben die im Archiv sind
        
        
    #plot final population with regard to the two objectives
    plotPopulationAndObjectiveValues(population, "Final Population")
    

    
    return bestFinalRoute
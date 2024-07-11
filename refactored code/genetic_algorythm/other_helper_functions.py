from .route import Route
from .city import City
from .mutation import *
from .breeding import *
from .selection import *


import numpy as np, random, operator, pandas as pd, matplotlib.pyplot as plt

#put into ranking file?
def rankRoutes(population:list[Route], objectiveNrUsed)-> list[tuple[int,float]]: 
    """
    Returns a sorted list of the ranked route. Element [0] has the best fitness.

    Ranking methods:
    1. DISTANCE BASED RANKING.
    2. STRESS BASED RANKING.
    3. PARETO FITNESS BASED RANKING.
    
    Returns:
    A list of tuples containing  
        [0] the population index of the actual Route (member of the population)
        [1] the respective fitness value that was being used to rank them (depending on the ranking method)
    """
    
   
    
    fitnessResults = list[tuple[int,float]] = []
    if (objectiveNrUsed == 1):
        for i in range(0,len(population)):
            #fitnessResults[i] = population[i].get_fitness_distance_based()
            fitnessResults.append((i,population[i].get_fitness_distance_based()))
    elif (objectiveNrUsed == 2):
        for i in range(0,len(population)):
            #fitnessResults[i] = population[i].get_fitness_stress_based()
            fitnessResults.append((i,population[i].get_fitness_stress_based()))
    elif (objectiveNrUsed == 3):
        #TODO: passender Aufruf der bestehenden Fitnessberechnung 
        print("Here is something missing")
        
    #print("ranked sorted routes: ", sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True))
    #if (objectiveNrUsed == 1):
        #print("before sorting ranked: ", fitnessResults)
    #sorted_values = sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True)
    sorted_values = sorted(fitnessResults, key = lambda x: x[1] , reverse = True)
     
    return sorted_values


#Provide Pareto-Based Fitness Calculation <<<<<<<<<<<<
# Dictionary bei dem für jedes Individuum die zugehörigen Werte gespeichert werden
# IndexNr:[distance,stress,[dominated solutions], [is dominated by solutions], R(i), F(i)]    
def rankRoutesBasedOnDominance(population):
    #store single fitness values per individuum
    fitnessValuesPerIndividuum = {}
    distance = 0
    stress = 0
    for i in range(0,len(population)):
        distance = Route(population[i]).routeDistance()
        stress = Route(population[i]).routeStress() 
        fitnessValuesPerIndividuum[i] = [distance, stress, [], [], 0, 0]
    #compute number of dominated solutions
    for i in range(0,len(population)):
       for j in range(0,len(population)):
           if (i != j):
              if (fitnessValuesPerIndividuum[i][0] < fitnessValuesPerIndividuum[j][0]
              and fitnessValuesPerIndividuum[i][1] < fitnessValuesPerIndividuum[j][1]):
                   fitnessValuesPerIndividuum[i][2].append(j) #add dominated solution
                   fitnessValuesPerIndividuum[j][3].append(i) #add dominating solution
    for i in range(0,len(population)):
        for domSol in fitnessValuesPerIndividuum[i][3]:
            fitnessValuesPerIndividuum[i][4] += len(fitnessValuesPerIndividuum[domSol][2])
    distanceValuesPerIndividuum = {}
    for i in range(0,len(population)):
        distanceValuesPerIndividuum[i] = []
        for j in range(0,len(population)):
           if (i != j):
               euclDistance = computeEuclideanDistance(fitnessValuesPerIndividuum[i][0],fitnessValuesPerIndividuum[j][0],
                                        fitnessValuesPerIndividuum[i][1], fitnessValuesPerIndividuum[j][1])
               distanceValuesPerIndividuum[i].append(euclDistance)
        distanceValuesPerIndividuum[i].sort()
    #determine k-nearest neighbour    
    k = int(np.floor((np.sqrt(len(population)))))
    if (k == 0):
        print("Something went wrong.")
        k = 1
    #index der Distanzberechnung, kter-Nachbar
    k -=1
    
    fitnessResults = {}
    for i in range(0,len(population)):
        #compute D(i)
        d_i = 1/ (distanceValuesPerIndividuum[i][k] + 2)
        fitnessValuesPerIndividuum[i][5] = fitnessValuesPerIndividuum[i][4] + d_i
        fitnessResults[i] = 1/fitnessValuesPerIndividuum[i][5] #damit größte Fitness = beste
    return fitnessResults 


def computeEuclideanDistance(distanceA, distanceB, stressA, stressB):
    return np.sqrt( (distanceA-distanceB)** 2 + (stressA-stressB)** 2) #should we use np here? i mean its supposed to be oone value only right?

#Put all steps together to create the next generation
 
#First, we rank the routes in the current generation using rankRoutes.
#We then determine our potential parents by running the selection function,
#    which allows us to create the mating pool using the matingPool function.
#Finally, we then create our new generation using the breedPopulation function 
# and then applying mutation using the mutatePopulation function. 

# put inside breeding file?
def nextGeneration(currentGen:list[Route], eliteSize, mutationRate, objectiveNrUsed, archiveUsed) -> list[Route]: 
   # rankRoutesBasedOnDominance(currentGen)
    #print("\n\n pop pre ranked",currentGen)

    popRanked:list[tuple[int,float]] = rankRoutes(currentGen,objectiveNrUsed)
    #print("\n\n pop ranked",popRanked)
    #print("\n\n next rankRoutes",rankRoutes)
    if (not archiveUsed):
        
        selectionResults:list[int] = selection(popRanked, eliteSize)
        #print("\n\n next selectionResults",matingpool)

        mating_pool:list[Route] = matingPool(currentGen, selectionResults)
        children:list[Route] = breedPopulation(mating_pool, eliteSize)
        #print("\n\n next children",children)
        nextGeneration:list[Route] = mutatePopulation(children, mutationRate,0)
    else:
        #<<<<< use archiv
        #TODO: ein festes Archiv vorsehen wie es im ursprünglichen SPEA2 vorgesehen ist 
        matingpool = selectionWithArchive(popRanked)
        #matingpool = matingPool(currentGen, selectionResults)
        archiveSize = determineNonDominatedArchiveSize(popRanked)
        children = breedPopulation(matingpool, archiveSize)
        

        #eliteSize is used to maintain solutions that should be in an archive
        nextGeneration = mutatePopulation(children, mutationRate, eliteSize)
        
    #print("\n\n next generation",nextGeneration)
    return nextGeneration
     
def getCityBasedOnNr(cityList,nr):
    if (nr <= 0 or nr > len(cityList)):
        print("Something is wrong!")
        return cityList[0]
    else:
        return cityList[nr-1]  
    
    

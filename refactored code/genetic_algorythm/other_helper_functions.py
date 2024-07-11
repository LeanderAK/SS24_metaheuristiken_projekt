from .route import Route
from .city import City
from .mutation import *
from .breeding import *
from .selection import *


import numpy as np, random, operator, pandas as pd, matplotlib.pyplot as plt


def rankRoutes(population:list[Route], objectiveNrUsed): #-> list[Route] thats ot what it returns, what does it return actually?
    """
    Returns a sorted list of the ranked route. Element [0] has the best fitness.

    Ranking methods:
    1. DISTANCE BASED RANKING.
    2. STRESS BASED RANKING.
    3. PARETO FITNESS BASED RANKING.
    """
    
    fitnessResults = {}
    if (objectiveNrUsed == 1):
        for i in range(0,len(population)):
            #fitnessResults[i] = Route(population[i]).routeFitnessDistanceBased()
            fitnessResults[i] = population[i].routeFitnessDistanceBased()
    elif (objectiveNrUsed == 2):
        for i in range(0,len(population)):
            fitnessResults[i] = population[i].routeFitnessStressBased()
    elif (objectiveNrUsed == 3):
        fitnessResults = rankRoutesBasedOnDominance(population=population)
    #print("sorted routes: ", sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True))

    return sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True)

#Provide Pareto-Based Fitness Calculation <<<<<<<<<<<<
# Dictionary bei dem für jedes Individuum die zugehörigen Werte gespeichert werden
# IndexNr:[distance,stress,[dominated solutions], [is dominated by solutions], R(i), F(i)]    
def rankRoutesBasedOnDominance(population):
    #store single fitness values per individuum
    fitnessValuesPerIndividuum = {}
    distance = 0
    stress = 0
    for i in range(0,len(population)):
        distance = population[i].routeDistance()
        stress = population[i].routeStress() 
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

def nextGeneration(currentGen:list[Route], eliteSize, mutationRate, objectiveNrUsed, archiveUsed, archiveSize = None, archive=None) -> list[Route]: 
   # rankRoutesBasedOnDominance(currentGen)
    popRanked = rankRoutes(currentGen,objectiveNrUsed)
    if (not archiveUsed):
        selectionResults = selection(popRanked, eliteSize)
        matingpool:list[Route] = matingPool(currentGen, selectionResults)
        children:list[Route] = breedPopulation(matingpool, eliteSize)
        nextGeneration = mutatePopulation(children, mutationRate,0)
        return nextGeneration
    else:
        # aktuelle generation: P(g)
        # aktuelles archiv: A(g)

        # Fitnessberechnung aller ergebnisse in P(g) und A(g)
        currentGenFitness = rankRoutes(currentGen, objectiveNrUsed=3)
        archiveFitness = rankRoutes(archive, objectiveNrUsed=3)

        # Kopiere alle nicht dominierten Individuen aus P(g) und A(g) in A(g+1)
        nonDominatedCurrentGen = determineNonDominatedArchive(currentGen, currentGenFitness)
        nonDominatedArchive = determineNonDominatedArchive(archive, archiveFitness)
        nextArchive = nonDominatedCurrentGen + nonDominatedArchive

        # N = archiveSize
        # |A(g+1)| > N: entferne nicht dominierte Individuen aus A(g+1)
        if len(nextArchive) > archiveSize:
            archiveFitness = rankRoutes(nextArchive, objectiveNrUsed=3)
            nonDominatedData = determineNonDominatedArchive(nextArchive, archiveFitness)
            nextArchive = [i for i in nextArchive if i not in nonDominatedData]
                    
        # |A(g+1)| < N: Fülle A(g+1) mit dominierten Individuen aus P(g) und A(g) auf
        if len(nextArchive) < archiveSize:
            dominatedCurrentGen = [i for i in currentGen if i not in nonDominatedCurrentGen]
            dominatedArchive = [i for i in archive if i not in nonDominatedArchive]
            nextArchive += dominatedCurrentGen + dominatedArchive
            
        # Turnierselektion von A(g+1)
        nextArchiveFitness = rankRoutes(nextArchive, objectiveNrUsed=3)
        selectionResults = selectionWithArchive(nextArchiveFitness)


        matingpool = matingPool(currentGen, selectionResults)
        # Neue Population P(g+1)
        archiveSize = determineNonDominatedArchiveSize(popRanked)
        children = breedPopulation(matingpool, archiveSize)
        #eliteSize is used to maintain solutions that should be in an archive
        nextGeneration = mutatePopulation(children, mutationRate, eliteSize)

        return nextGeneration, nextArchive
     
def getCityBasedOnNr(cityList,nr):
    if (nr <= 0 or nr > len(cityList)):
        print("Something is wrong!")
        return cityList[0]
    else:
        return cityList[nr-1]  
    
    

# -*- coding: utf-8 -*-
"""
Created for Netzwerke & Metaheuristiken (Sommersemester 2024)

Modified version of https://github.com/ezstoltz/genetic-algorithm/blob/master/genetic_algorithm_TSP.ipynb
(description https://towardsdatascience.com/evolution-of-a-salesman-a-complete-genetic-algorithm-tutorial-for-python-6fe5d2b3ca35)

Modified for multicriteria TSP
"""

from typing import Optional
import numpy as np, random, operator, pandas as pd, matplotlib.pyplot as plt

#Create necessary classes and functions
#Create class to handle "cities


#Create a fitness function -> its a class



#Create our initial population
#Route generator
def create_random_route(cityList) -> Route:
    route = random.sample(cityList, len(cityList))
    return Route(route)

#Create first "population" (list of routes)
def initialPopulation(popSize, cityList, specialInitialSolutions: list[Route]):
    population:list[Route] = []
    
    #TODO: Hinzufügen der speziellen Initiallösungen aus specialInitialSolutions
    for i in range(len(specialInitialSolutions)):
        population.append(specialInitialSolutions[i])

    numberInitialSolutions = len(specialInitialSolutions)
    print ("Number of special initial solutions:" + str(numberInitialSolutions))
    #for i in range(0, popSize):
    for i in range(numberInitialSolutions, popSize):
        population.append(create_random_route(cityList))
    return population

#Create the genetic algorithm
#Rank individuals

def rankRoutes(population, objectiveNrUsed): #-> list[Route] thats ot what it returns, what does it return actually?
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
            fitnessResults[i] = Route(population[i]).routeFitnessDistanceBased()
    elif (objectiveNrUsed == 2):
        for i in range(0,len(population)):
            fitnessResults[i] = Route(population[i]).routeFitnessStressBased()
    elif (objectiveNrUsed == 3):
        #TODO: passender Aufruf der bestehenden Fitnessberechnung 
        print("Here is something missing")
        
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

#def compute_euclidian_distance_distance_only(distanceA ,distanceB ):
#    return np.sqrt((distanceA-distanceB)**2)
    
#def compute_euclidian_distance_stress_only(stressA, stressB):
#    return np.sqrt
    

#Create a selection function that will be used to make the list of parent routes
def selection(popRanked, eliteSize):
    selectionResults = []
    #TODO: Z.B. Turnierbasierte Selektion statt fitnessproportionaler Selektion
    # roulette wheel by calculating a relative fitness weight for each individual
    df = pd.DataFrame(np.array(popRanked), columns=["Index","Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()
    
    #We’ll also want to hold on to our best routes, so we introduce elitism
    for i in range(0, eliteSize):
        selectionResults.append(popRanked[i][0])
    #we compare a randomly drawn number to these weights to select our mating pool
    for i in range(0, len(popRanked) - eliteSize):
        pick = 100*random.random()
        for i in range(0, len(popRanked)):
            if pick <= df.iat[i,3]:
                selectionResults.append(popRanked[i][0])
                break
    return selectionResults
    
def selectionWithArchive(popRanked):
    selectionResults = []
    #TODO: Z.B. Turnierbasierte Selektion statt fitnessproportionaler Selektion
    # roulette wheel by calculating a relative fitness weight for each individual
    df = pd.DataFrame(np.array(popRanked), columns=["Index","Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()
    
    #We’ll also want to hold on to our best routes, so we introduce elitism
    #here wie hold all non-dominated solutions
    #TODO: ein festes Archiv vorsehen wie es im ursprünglichen SPEA2 vorgesehen ist 
    for i in range(0, len(popRanked)):
        if (popRanked[i][1] > 1):
            selectionResults.append(popRanked[i][0])
    currentArchiveSize = len(selectionResults)

    #we compare a randomly drawn number to these weights to select our mating pool
    for i in range(0, len(popRanked) - currentArchiveSize):
        pick = 100*random.random()
        for i in range(0, len(popRanked)):
            if pick <= df.iat[i,3]:
                selectionResults.append(popRanked[i][0])
                break
    return selectionResults

#Create mating pool
def matingPool(population, selectionResults):
    matingpool = []
    for i in range(0, len(selectionResults)):
        index = selectionResults[i]
        matingpool.append(population[index])
    return matingpool

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
def breedPopulation(matingpool, eliteSize):
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

#Create function to mutate a single route
#we’ll use swap mutation.
#This means that, with specified low probability, 
#two cities will swap places in our route.
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

def determineNonDominatedArchive(currentGen, popRanked):
    archive = []
    for i in range(0, len(popRanked)):
        if (popRanked[i][1] > 1):
            archive.append(currentGen[popRanked[i][0]])
    #-------Prüfung auf Gleichheit bei Bedarf auskommentieren 
    sameSolutions = []
    for i in range(0, len(archive)-1):
        for j in range(i+1, len(archive)):
            if isSameSolution(archive[i], archive[j]):
                sameSolutions.append(j)
    newArchive = []
    for i in range(0, len(archive)):
        if (not sameSolutions.__contains__(i)):
            newArchive.append(archive[i])
    return newArchive

def determineNonDominatedArchiveSize(popRanked):
    archiveSize = 0
    for i in range(0, len(popRanked)):
        if (popRanked[i][1] > 1):
            archiveSize += 1
    return archiveSize

def isSameSolution(individuumA, individuumB):
    length = len(individuumA)
    i = 0
    isSameSolution = True
    while i < length and isSameSolution:
        if (not (individuumA[i].nr == individuumB[i].nr)):
            isSameSolution = False
            break
        i+=1
    return isSameSolution
    

#Put all steps together to create the next generation
 
#First, we rank the routes in the current generation using rankRoutes.
#We then determine our potential parents by running the selection function,
#    which allows us to create the mating pool using the matingPool function.
#Finally, we then create our new generation using the breedPopulation function 
# and then applying mutation using the mutatePopulation function. 

def nextGeneration(currentGen, eliteSize, mutationRate, objectiveNrUsed, archiveUsed): 
   # rankRoutesBasedOnDominance(currentGen)
    popRanked = rankRoutes(currentGen,objectiveNrUsed)
    if (not archiveUsed):
        selectionResults = selection(popRanked, eliteSize)
        matingpool = matingPool(currentGen, selectionResults)
        children = breedPopulation(matingpool, eliteSize)
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

#Final step: create the genetic algorithm
def plotPopulationAndObjectiveValues(population,title):
    distance = []
    stress = []
    for route in population:
        distance.append(Route(route).routeDistance())
        stress.append(Route(route).routeStress())
    plt.scatter(distance,stress,marker = "o",color="black")
    plt.ylabel('Stress')
    plt.xlabel('Distance')
    plt.title(title)
    plt.show()
        

def geneticAlgorithm(objectiveNrUsed, specialInitialSolutions: list[Route], population, popSize, eliteSize, mutationRate, generations):
    #create initial population
    pop = initialPopulation(popSize, population, specialInitialSolutions)
    
    archiveUsed = False
    
    #print("initial population: ", pop)
    
    #provide statistics about best initial solution with regard to chosen objective
    if (objectiveNrUsed == 1 or objectiveNrUsed == 2):
        print("Initial objective: " + str(1 / rankRoutes(pop,objectiveNrUsed)[0][1]))
        bestRouteIndex = rankRoutes(pop,objectiveNrUsed)[0][0]
        bestRoute = pop[bestRouteIndex]
        print("Initial distance : " + str(Route(bestRoute).routeDistance()))
        print("Initial stress:    " + str(Route(bestRoute).routeStress()))
        plotRoute(bestRoute, "Best initial route")
    elif(objectiveNrUsed == 3):
        print("Initial highest fitness value: " + str(rankRoutes(pop,objectiveNrUsed)[0][1]))
        print("Initial best distance value: " + str(1/ rankRoutes(pop,1)[0][1]))
        print("Initial best stress value: " + str(1/ rankRoutes(pop,2)[0][1]))
        archiveUsed = True
    
    #plot intial population with regard to the two objectives
    plotPopulationAndObjectiveValues(pop, "Initial Population")
    
    #store infos to plot progress when finished
    progressDistance = []
    progressDistance.append(1 / rankRoutes(pop,1)[0][1])
    progressStress = []
    progressStress.append(1 / rankRoutes(pop,2)[0][1])
    
    
    #create new generations of populations
    for i in range(0, generations):
        print(i, end=", ")
        pop = nextGeneration(pop, eliteSize, mutationRate,objectiveNrUsed,archiveUsed)
        #store infos to plot progress when finished
        progressDistance.append(1 / rankRoutes(pop,1)[0][1])
        progressStress.append(1 / rankRoutes(pop,2)[0][1])
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
    
    #provide statistics about best final solution with regard to chosen objective
    if (objectiveNrUsed == 1 or objectiveNrUsed == 2):
        print("Final objective: " + str(1 / rankRoutes(pop,objectiveNrUsed)[0][1])) 
        bestRouteIndex = rankRoutes(pop,objectiveNrUsed)[0][0]
        bestRoute = pop[bestRouteIndex]
        print("Final distance : " + str(Route(bestRoute).routeDistance()))
        print("Final stress:    " + str(Route(bestRoute).routeStress()))
        
        #Provide special initial solutions    <<<<<<<<<<<
        #print city Indizes for initial solution
        bestRouteIndizes = []
        for city in bestRoute:
            bestRouteIndizes.append(city.nr)
    
        print("---- ")
        print("City Numbers of Best Route")
        print(bestRouteIndizes)
        print("---- ")
        plotRoute(bestRoute, "Best final route")
        
    elif(objectiveNrUsed == 3):
        print("Final highest fitness value: " + str(rankRoutes(pop,objectiveNrUsed)[0][1]))
        print("Final best distance value: " + str(1/ rankRoutes(pop,1)[0][1]))
        print("Final best stress value: " + str(1/ rankRoutes(pop,2)[0][1]))
        bestRouteIndex = rankRoutes(pop,objectiveNrUsed)[0][0]
        bestRoute = pop[bestRouteIndex]
        #TODO: ein festes Archiv vorsehen wie es im ursprünglichen SPEA2 vorgesehen ist
        # dann alle Lösungen ausgeben die im Archiv sind
        
        
    #plot final population with regard to the two objectives
    plotPopulationAndObjectiveValues(pop, "Final Population")
    

    
    return bestRoute

#Running the genetic algorithm
#Create list of cities
cityList:list[City] = []

random.seed(44)
for i in range(1,26):
    cityList.append(City(nr= i, traffic=int(random.random()*40), x=int(random.random() * 200), y=int(random.random() * 200)))
    
print(cityList)


def plotRoute(cityList, title):
    x = []
    y = []
    for item in cityList:
        x.append(item.x)
        y.append(item.y)
        plt.annotate(item.nr,(item.x,item.y))
    x.append(cityList[0].x)
    y.append(cityList[0].y)
    plt.plot(x,y,marker = "x")
    plt.ylabel('Y-Coordinate')
    plt.xlabel('X-Coordinate')
    plt.title(title)
    plt.show()    

def getCityBasedOnNr(cityList,nr):
    if (nr <= 0 or nr > len(cityList)):
        print("Something is wrong!")
        return cityList[0]
    else:
        return cityList[nr-1]     
    
#Provide special initial solutions     <<<<<<<<<<<
cityNumbersRoute1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]


route1 = []
for nr in cityNumbersRoute1:
    route1.append(getCityBasedOnNr(cityList,nr))
    

def get_special_initial_solutions() -> list[Route]:
    
    # initial solution 1 -> distance
    potential_next_cities_d = cityList.copy()

    initial_solution_low_distance:list[City] = [potential_next_cities_d[0]]
    potential_next_cities_d.remove(potential_next_cities_d[0])

    while len(potential_next_cities_d) > 0:        
        lowest_distance_so_far = float('inf')
        next_city:City = None
        
        for i in range(len(potential_next_cities_d)):
            
            distance = initial_solution_low_distance[len(initial_solution_low_distance)-1].distance(potential_next_cities_d[i])
            if(distance < lowest_distance_so_far):
                lowest_distance_so_far = distance
                next_city = potential_next_cities_d[i]
                #print(f"distance between {initial_solution_low_distance[len(initial_solution_low_distance)-1]} and {potential_next_cities_d[i]} is {distance}")
                
        initial_solution_low_distance.append(next_city)
        potential_next_cities_d.remove(next_city)
     
    print("\n initial solution cities: ", initial_solution_low_distance)
    distance_optimised_route = Route(initial_solution_low_distance)
     
    # # initial solution 2 -> stress
    # potential_next_cities_s = cityList.copy()

    # initial_solution_low_stress:list[City] = [potential_next_cities_s[0]]
    # potential_next_cities_s.remove(potential_next_cities_s[0])

    # while len(potential_next_cities_s) > 0:        
    #     lowest_stress_so_far = float('inf')
    #     next_city = None
        
    #     for i in range(len(potential_next_cities_s)):
    #         stress = initial_solution_low_distance[len(initial_solution_low_distance)-1].stress(potential_next_cities_s[i])
    #         if(stress < lowest_stress_so_far):
    #             lowest_stress_so_far = stress
    #             next_city = potential_next_cities_s[i]
                
    #     initial_solution_low_distance.append(next_city)
    #     potential_next_cities_s.remove(next_city)
     
     
     
    # print("solution low stress: ", initial_solution_low_stress)
    print("distance_optimised_route type: ",type(distance_optimised_route))
    print("solution low distance: ", initial_solution_low_distance)
    print("solution low distance - distance : ", distance_optimised_route.routeDistance())
    
    
    #return [initial_solution_low_distance, initial_solution_low_stress]
    return [distance_optimised_route,distance_optimised_route,distance_optimised_route,distance_optimised_route]
        


initialSolutionsList = get_special_initial_solutions()
#TODO: Spezielle Intiallösungen der initialSolutionsList übergeben

# initial solutions - have one solutions that was created by connecting the shortest euclidian distances and one that was created connecting the shortest stress distances


    
    
#Run the genetic algorithm
#modify parameters popSize, eliteSize, mutationRate, generations to search for the best solution
#modify objectiveNrUsed to use different objectives:
# 1= Minimize distance, 2 = Minimize stress, 3 = MinimizeBoth
bestRoute = geneticAlgorithm(objectiveNrUsed=1, specialInitialSolutions = initialSolutionsList, population=cityList,
                             popSize=100, eliteSize=20, mutationRate=0.01, generations=500)
#print(bestRoute)

#plotRoute(bestRoute, "Best final route")
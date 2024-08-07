from .fitness import Fitness
import operator
from .other_helper_functions import *
from pymoo.indicators.hv import HV
import numpy as np


def rankRoutes(population, objectiveNrUsed) -> list[tuple[int,float]]:
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
    
    fitnessResults = {}
    if (objectiveNrUsed == 1):
        for i in range(0,len(population)):
            fitnessResults[i] = Fitness(population[i]).routeFitnessDistanceBased()
    elif (objectiveNrUsed == 2):
        for i in range(0,len(population)):
            fitnessResults[i] = Fitness(population[i]).routeFitnessStressBased()
    elif (objectiveNrUsed == 3):
        fitnessResults = rankRoutesBasedOnDominance(population)
        
    #print("ranked sorted routes: ", sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True))
   ## if (objectiveNrUsed == 1):
    #    print("before sorting ranked: ", fitnessResults)
    sorted_values = sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True)
   # if (objectiveNrUsed == 1):
     #   print("after sorting ranked: ", sorted_values)
    
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
        distance = Fitness(population[i]).routeDistance()
        stress = Fitness(population[i]).routeStress() 
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

def get_hypervolume_value(pareto_front_city_list:list[list[City]]):
    reference_point = [3000,7000] #this is a maximum point throughout almost every generation
    
    pareto_front = []
    
    for route in pareto_front_city_list:
        pareto_front.append([Fitness(route).routeDistance(),Fitness(route).routeStress()])
    
    pareto_front = np.array(pareto_front)
    
    hv_indicator = HV(ref_point=reference_point)
    hypervolume_value = hv_indicator.do(pareto_front)
    
    
   
    
    return hypervolume_value

def reformat_hypervolume_value(value):
    value = int(value)
     #reformat value
    # Reverse the string (for easier insertion of spaces)
    reversed_str = str(value)[::-1] 
    # Insert spaces every 3 characters
    formatted_str = " ".join(reversed_str[i:i+3] for i in range(0, len(reversed_str), 3))
    # Reverse back to the original order
    formatted_number = formatted_str[::-1]
    return formatted_number
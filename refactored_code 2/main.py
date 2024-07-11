
from genetic_algorythm.route import Fitness
from genetic_algorythm.city import City
from genetic_algorythm.other_helper_functions import *
from genetic_algorythm.genetic_algorythm import geneticAlgorithm
import numpy as np, random, operator, pandas as pd, matplotlib.pyplot as plt


#Running the genetic algorithm
#Create list of cities
all_cities:list[City] = []

random.seed(44)
for i in range(1,26):
    all_cities.append(City(nr= i, traffic=int(random.random()*40), x=int(random.random() * 200), y=int(random.random() * 200)))
    
print(all_cities)

#Provide special initial solutions     <<<<<<<<<<<
cityNumbersRoute1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]

route1 = []
for nr in cityNumbersRoute1:
    route1.append(getCityBasedOnNr(all_cities,nr))
    
#initialSolutionsList = get_special_initial_solutions(all_cities)
initialSolutionsList:list[Fitness] = []
#skip for now see, weather it still works


#Run the genetic algorithm
#modify parameters popSize, eliteSize, mutationRate, generations to search for the best solution
#modify objectiveNrUsed to use different objectives:
# 1= Minimize distance, 2 = Minimize stress, 3 = MinimizeBoth

# bestRoute = geneticAlgorithm(objectiveNrUsed=1, specialInitialSolutions = initialSolutionsList, population_genes=all_cities,
#                               popSize=5, eliteSize=2, mutationRate=0.01, generations=2)

bestRoute = geneticAlgorithm(objectiveNrUsed=1, specialInitialSolutions = initialSolutionsList, population_genes=all_cities,
                            popSize=200, eliteSize=20, mutationRate=0.01, generations=500)
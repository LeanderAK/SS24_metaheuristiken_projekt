
from genetic_algorythm.fitness import Fitness
from genetic_algorythm.city import City
from genetic_algorythm.initial_population import City
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
    route1.append(getCityBasedOnNr(all_cities,nr)) #to delete? 
    
#initialSolutionsList:list[list[City]] = get(all_cities)
#initialSolutionsList:list[Fitness] = []
#skip for now see, weather it still works


#Run the genetic algorithm
#modify parameters popSize, eliteSize, mutationRate, generations to search for the best solution
#modify objectiveNrUsed to use different objectives:
# 1= Minimize distance, 2 = Minimize stress, 3 = MinimizeBoth

# bestRoute = geneticAlgorithm(objectiveNrUsed=1, specialInitialSolutions = initialSolutionsList, population_genes=all_cities,
#                               popSize=5, eliteSize=2, mutationRate=0.01, generations=2)

# bestRoute = geneticAlgorithm(objectiveNrUsed=1, population_genes=all_cities,
#                             popSize=200, eliteSize=20, mutationRate=0.01, generations=500)


def evaluate_ga_parameters(objectiveNrUsed, initialPopNrUsed, selectionNrUsed, population_genes,
                                popSize, eliteSize, breeding_rate, mutationRate, generations, archiveSize):
    
    bestRoute, bestRouteFitness = geneticAlgorithm(objectiveNrUsed=objectiveNrUsed, initialPopNrUsed=initialPopNrUsed, selectionNrUsed=selectionNrUsed, population_genes=population_genes,
                                popSize=popSize, eliteSize=eliteSize, breeding_rate=breeding_rate, mutationRate=mutationRate, generations=generations, archiveSize=archiveSize)
    
    return bestRouteFitness

param_space = {
    'popSize': [100,200],
    'eliteSize': [10, 20],
    'breeding_rate': [0.1, 0.3],
    'mutationRate': [0.002, 0.001, 0.0005],
    'generations': [400, 500],
    'archiveSize': [10, 20]
}

# List to store results
results = []

n_samples = 20
for _ in range(n_samples):
    popSize = random.choice(param_space['popSize'])
    eliteSize = random.choice(param_space['eliteSize'])
    breeding_rate = random.choice(param_space['breeding_rate'])
    mutationRate = random.choice(param_space['mutationRate'])
    generations = random.choice(param_space['generations'])
    archiveSize = random.choice(param_space['archiveSize'])
    
    score = evaluate_ga_parameters(
        objectiveNrUsed = 3, 
        initialPopNrUsed = 1, 
        selectionNrUsed = 2, 
        population_genes = all_cities,
        popSize = popSize,
        eliteSize = eliteSize, 
        breeding_rate = breeding_rate, 
        mutationRate = mutationRate, 
        generations = generations, 
        archiveSize = archiveSize
    )
    results.append((score, popSize, eliteSize, breeding_rate, mutationRate, generations, archiveSize))

# Find the best parameters
best_result = min(results, key=lambda x: x[0])
best_score, best_popSize, best_eliteSize, best_breeding_rate, best_mutationRate, best_generations, best_archiveSize = best_result

print(f'Best Fitness Score: {best_score}')
print(f'Best Parameters - popSize: {best_popSize}, eliteSize: {best_eliteSize}, breedingRate: {best_breeding_rate} mutationRate: {best_mutationRate}, generations: {best_generations}, archiveSize: {best_archiveSize}')

    


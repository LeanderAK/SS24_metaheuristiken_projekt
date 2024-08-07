
import yaml
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
    

# Load settings from config.yaml
with open('refactored_code/config.yaml', 'r') as file:
    config_yaml = yaml.safe_load(file)

    results = []
    for _ in range(config_yaml.get('randomSearchIterations', 1)):
        
        popSizeInstance = random.choice(config_yaml['popSize'])
        eliteSizeInstance = random.choice(config_yaml['eliteSize'])
        breeding_rateInstance = random.choice(config_yaml['breeding_rate'])
        mutationRateInstance = random.choice(config_yaml['mutationRate'])
        generationsInstance = random.choice(config_yaml['generations'])
        archiveSizeInstance = random.choice(config_yaml['archiveSize'])
        
        bestRoute, bestFitnessScore = geneticAlgorithm(
            objectiveNrUsed=config_yaml['objectiveNrUsed'], 
            initialPopNrUsed=config_yaml['initialPopNrUsed'], 
            selectionNrUsed=config_yaml['selectionNrUsed'], 
            population_genes=all_cities,
            popSize=popSizeInstance,
            eliteSize=eliteSizeInstance, 
            breeding_rate=breeding_rateInstance, 
            mutationRate=mutationRateInstance, 
            generations=generationsInstance, 
            archiveUsed=config_yaml['archiveUsed'],
            archiveSize=archiveSizeInstance, 
            plot_level=config_yaml['plotLevel']
        )
        results.append((bestFitnessScore, popSizeInstance, eliteSizeInstance, breeding_rateInstance, mutationRateInstance, generationsInstance, archiveSizeInstance))

    # Find the best parameters
    best_result = min(results, key=lambda x: x[0])
    best_score, best_popSize, best_eliteSize, best_breeding_rate, best_mutationRate, best_generations, best_archiveSize = best_result

    print(f'Best Fitness Score: {best_score}')
    print(f'Best Parameters - popSize: {best_popSize}, eliteSize: {best_eliteSize}, breedingRate: {best_breeding_rate} mutationRate: {best_mutationRate}, generations: {best_generations}, archiveSize: {best_archiveSize}')


import random
from .route import Route
from .city import City

#Create function to mutate a single route
#we’ll use swap mutation.
#This means that, with specified low probability, 
#two cities will swap places in our route.
def mutate(individual:Route, mutationRate) -> Route:
    assert isinstance(individual, Route)
    cities: list[City] = individual.get_cities()
    
    for swapped in range(individual.number_of_cities()):
        if(random.random() < mutationRate):
            swapWith = int(random.random() * individual.number_of_cities())
            
            city1 = cities[swapped]
            city2 = cities[swapWith]
            
            cities[swapped] = city2
            cities[swapWith] = city1
    individual.cities = cities
    return individual

#Create function to run mutation over entire population
def mutatePopulation(population:list[Route], mutationRate, eliteSize) -> list[Route]:
    
    assert isinstance(population, list)
    assert all(isinstance(route, Route) for route in population)
    
    mutatedPop:list[Route] = []
    
    #mating pool is sorted in order of fitness
    #here elitism instead of fixed archive
    #TODO: ein festes Archiv vorsehen wie es im ursprünglichen SPEA2 vorgesehen ist 
    for i in range(0, eliteSize):
        mutatedPop.append(population[i])
    for i in range(eliteSize, len(population)):
    #for ind in range(0, len(population)):
        mutatedInd = mutate(population[i], mutationRate)
        mutatedPop.append(mutatedInd)
    return mutatedPop
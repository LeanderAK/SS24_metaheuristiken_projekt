
import random

from .other_helper_functions import *
from .fitness import Fitness
from .city import City

#Create our initial population
#Route generator
def createRoute(cityList)->list[City]:
    route = random.sample(cityList, len(cityList))
    #for item in route:
    #    print(f"inside list: type is city? {isinstance(item,City)}")
    print(f"")
    return route

#Create first "population" (list of routes)
def initialPopulation(initialPopNrUsed:int , popSize, cityList) -> list[list[City]]:
    population = []
    
    #TODO: Hinzufügen der speziellen Initiallösungen aus specialInitialSolutions
    specialInitialSolutions = get_special_initial_solutions(initialPopNrUsed, cityList)
    
    for i in range(len(specialInitialSolutions)):
        population.append(specialInitialSolutions[i])

    numberInitialSolutions = len(specialInitialSolutions)
    print ("Number of special initial solutions:" + str(numberInitialSolutions))
    #for i in range(0, popSize):
    for i in range(numberInitialSolutions, popSize):
        population.append(createRoute(cityList))
    return population

def get_special_initial_solutions(initialPopNrUsed, all_cities:list[City]) -> list[list[City]]:
    """
    initialPopNrUsed
    1: no initial population
    2: smallest distances for distance calculation and smallest distance for stress calculation
    3: best solutions for stress and distance from objective 1 and 2 
    """
    
    if(initialPopNrUsed == 1):
        return []
    
    elif(initialPopNrUsed == 2):     
        # initial solution 1 -> optimise distance programatically 
        potential_next_cities_d = all_cities.copy()

        initial_solution_low_distance:list[City] = [potential_next_cities_d[0]]
        potential_next_cities_d.remove(potential_next_cities_d[0])

        while len(potential_next_cities_d) > 0:        
            lowest_distance_so_far = float('inf')
            #next_city:City = None
            
            for i in range(len(potential_next_cities_d)):
                
                distance = initial_solution_low_distance[len(initial_solution_low_distance)-1].distance(potential_next_cities_d[i])
                if(distance < lowest_distance_so_far):
                    lowest_distance_so_far = distance
                    next_city = potential_next_cities_d[i]
                    #print(f"distance between {initial_solution_low_distance[len(initial_solution_low_distance)-1]} and {potential_next_cities_d[i]} is {distance}")
                    
            initial_solution_low_distance.append(next_city)
            potential_next_cities_d.remove(next_city)
        
        print("\n initial solution cities: ", initial_solution_low_distance)
        distance_optimised_fitness = Fitness(initial_solution_low_distance)
        
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
        #print("distance_optimised_route type: ",type(distance_optimised_route))
        #print("solution low distance: ", initial_solution_low_distance)
        #print("solution low distance - distance : ", distance_optimised_route.routeDistance())
        
        
        #return [initial_solution_low_distance, initial_solution_low_stress]
        return [initial_solution_low_distance,initial_solution_low_distance,initial_solution_low_distance,initial_solution_low_distance]
    
    elif initialPopNrUsed ==3:
        best_distance_ids =  [20, 14, 17, 24, 18, 9, 8, 4, 12, 25, 1, 10, 22, 6, 13, 23, 3, 7, 19, 2, 21, 11, 16, 5, 15]
        
        best_stress_ids = [18, 6, 2, 16, 4, 20, 10, 5, 25, 13, 1, 11, 7, 14, 22, 23, 19, 9, 8, 17, 12, 21, 3, 15, 24]
        
        distance_optimized_solution:list[City] = convert_city_numbers_list_to_city_list(best_distance_ids,all_cities)
        stress_optimised_solution:list[City] = convert_city_numbers_list_to_city_list(best_stress_ids,all_cities)
        
        return [distance_optimized_solution, distance_optimized_solution, stress_optimised_solution, stress_optimised_solution]
        

    return []
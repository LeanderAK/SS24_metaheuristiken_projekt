import numpy as np
from .city import City


def computeEuclideanDistance(distanceA, distanceB, stressA, stressB):
    return np.sqrt( (distanceA-distanceB)** 2 + (stressA-stressB)** 2)

def getCityBasedOnNr(cityList,nr):
    if (nr <= 0 or nr > len(cityList)):
        print("Something is wrong!")
        return cityList[0]
    else:
        return cityList[nr-1] 
    
def convert_city_numbers_list_to_city_list(number_list:list[int],city_list:list[City]):
    
    new_city_list:list[City] = []
    
    for number in number_list:
        new_city_list.append(getCityBasedOnNr(city_list,number))
        
    return new_city_list
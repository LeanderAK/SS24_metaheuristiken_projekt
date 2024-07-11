import numpy as np


def computeEuclideanDistance(distanceA, distanceB, stressA, stressB):
    return np.sqrt( (distanceA-distanceB)** 2 + (stressA-stressB)** 2)

def getCityBasedOnNr(cityList,nr):
    if (nr <= 0 or nr > len(cityList)):
        print("Something is wrong!")
        return cityList[0]
    else:
        return cityList[nr-1] 
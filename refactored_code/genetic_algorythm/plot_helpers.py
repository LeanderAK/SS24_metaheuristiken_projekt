#Final step: create the genetic algorithm
from matplotlib import pyplot as plt
from .fitness import Fitness


def plotPopulationAndObjectiveValues(population,title, special_colored_population = None):
    distance = []
    stress = []
    for route in population:
        distance.append(Fitness(route).routeDistance())
        stress.append(Fitness(route).routeStress())
    plt.scatter(distance,stress,marker = "o",color="black")
    
    if(special_colored_population is not None):
        special_distance = []
        special_stress = []
        for route in special_colored_population:
            special_distance.append(Fitness(route).routeDistance())
            special_stress.append(Fitness(route).routeStress())
        plt.scatter(special_distance,special_stress,marker = "o",color="red")

    plt.ylabel('Stress')
    plt.xlabel('Distance')
    plt.title(title)
    plt.show()
    
    

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
    
    
def plotProgress(progress: list[float], label:str):
    plt.plot(progress)
    plt.ylabel(label)
    plt.xlabel('Generation')
    plt.title(f'Progress of {label} Minimization')
    plt.show()

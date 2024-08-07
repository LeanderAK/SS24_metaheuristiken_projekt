#Final step: create the genetic algorithm
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

from .city import City
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
    if(label == "Hypervolume"):
        plt.title(f'Progress of {label} Maximization')
    else:
        plt.title(f'Progress of {label} Minimization')
    plt.show()

def plot_hypervolume(city_list:list[list[City]]):
    "city list - array of arrays wiht [x,y] values"
    
    distance = []
    stress = []
    for route in city_list:
        distance.append(Fitness(route).routeDistance())
        stress.append(Fitness(route).routeStress())
    
    
    reference_point = [3000,7000] #this is a maximum point throughout almost every generation
    
    plt.figure(figsize=(8,6))
    # Draw front only
    plt.scatter(distance, stress, label='Pareto Front')
    # Draw volume
    for point in zip(distance,stress):
        # plt.fill_between([point[0], reference_point[0]], [point[1],reference_point[1]], alpha=1,color='orange')
        width = reference_point[0] - point[0]
        height = reference_point[1] - point[1]
        rect = Rectangle((point[0], point[1]), width, height, color='orange', alpha=1)
        plt.gca().add_patch(rect)
        
    plt.ylabel('Stress')
    plt.xlabel('Distance')
    plt.title('Pareto Front and Hypervolume')
    plt.legend()
    plt.grid(True)
    plt.show()
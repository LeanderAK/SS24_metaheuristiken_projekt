from matplotlib import pyplot as plt
from .route import Route
from .city import City


def plotPopulationAndObjectiveValues(population:list[Route],title):
    distance = []
    stress = []
    for route in population:
        distance.append(route.routeDistance())
        stress.append(route.routeStress())
    plt.scatter(distance,stress,marker = "o",color="black")
    plt.ylabel('Stress')
    plt.xlabel('Distance')
    plt.title(title)
    plt.show()
    
    
def plotRoute(route:Route, title):
    cityList:list[City] = route.get_cities()
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
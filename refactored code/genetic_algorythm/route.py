from .city import City

class Route:
    def __init__(self, cities: list[City]):
        
        assert isinstance(cities, list)
        assert all(isinstance(city, City) for city in cities)
        self.cities:list[City] = cities
        self.distance = 0
        self.stress = 0
        self.fitnessDistanceBased = 0.0
        self.fitnessStressBased = 0.0
    
    #fitness calculation for objective: distance
    #1. distance calculation
    def routeDistance(self):
        if self.distance ==0:
            pathDistance = 0
            #print("eror check: route? ", type(self.cities))
            for i in range(0, len(self.cities)):
                fromCity = self.cities[i]
                toCity = None
                if i + 1 < len(self.cities):
                    toCity = self.cities[i + 1]
                else:
                    toCity = self.cities[0]
                # print("error check 1", fromCity)
                # print("error check 2", toCity)
                # print("error check 3", type(fromCity))
                # print("error check 3", type(toCity))
                # print("error check 4", fromCity.distance(toCity))
                pathDistance += fromCity.distance(toCity)
            self.distance = pathDistance
        return self.distance
    
    def get_cities(self):
        #todo cache this
        return self.cities
    
    def number_of_cities(self):
        #TODO cache this
        return len(self.cities)
    
    #2. fitness = 1/distance
    def get_fitness_distance_based(self):
        if self.fitnessDistanceBased == 0:
            self.fitnessDistanceBased = 1 / float(self.routeDistance())
        return self.fitnessDistanceBased
    
    #fitness calculation for objective: stress
    #1. stress calculation
    def routeStress(self):
        if self.stress ==0:
            pathStress = 0
            for i in range(0, len(self.cities)):
                fromCity = self.cities[i]
                toCity = None
                if i + 1 < len(self.cities):
                    toCity = self.cities[i + 1]
                else:
                    toCity = self.cities[0]
                pathStress += fromCity.stress(toCity)
            self.stress = pathStress
        return self.stress
    
    #2. fitness = 1/stress
    def get_fitness_stress_based(self):
        if self.fitnessStressBased == 0:
            self.fitnessStressBased = 1 / float(self.routeStress())
        return self.fitnessStressBased
    
    def __repr__(self):
        #return f"R d{self.routeDistance()} sF{self.fitnessDistanceBased()}"
        return str(self.cities)
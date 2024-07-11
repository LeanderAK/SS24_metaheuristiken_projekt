import numpy as np

class City:
    def __init__(self, nr, traffic, x, y):
        self.nr = nr
        #attribute used for stress calculation
        self.traffic = traffic
        #coordinates used for distance calculation
        self.x = x
        self.y = y
    
    #calculate distance to other city  
    def distance(self, city):
        xDis = abs(self.x - city.x)
        yDis = abs(self.y - city.y)
        distance = np.sqrt((xDis ** 2) + (yDis ** 2))
        return distance
    
    #calculate stress on way to other city
    def stress(self,city):
        stress = self.traffic*city.traffic
        if (self.nr > city.nr):
            if self.nr % city.nr == 0:
                stress = stress /2.5
        elif self.nr > 1 and city.nr % self.nr == 0:
            stress = stress /2.5
        return stress

    #provide information about city
    def __repr__(self):
        return "C"+str(self.nr)+"_"+"(" + str(self.x) + "," + str(self.y) + ")_(T:"+str(self.traffic) +")"
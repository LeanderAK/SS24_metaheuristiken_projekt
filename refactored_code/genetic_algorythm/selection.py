import numpy as np, random, operator, pandas as pd

#Create a selection function that will be used to make the list of parent routes
def selection(selectionNrUsed:int, popRanked: list[tuple[int,float]], eliteSize) -> list[int]:
    """
    selectionNrUsed: 
        1: fitnessproportional solution
        2: tournament-based selection
        3: roulete-wheel selection
    
    Return a list of the selected route indexes
    
    popRanked should be a list[tuple[int,float]]  
        [0] left int:  the population index of the actual Route
        [1] right float:  the respective fitness value that was being used
    """
    
    selectionResults = []
    
     #Elitism
    for i in range(0, eliteSize):
        selectionResults.append(popRanked[i][0])
    
    if selectionNrUsed == 1: # fitness proportional
        df = pd.DataFrame(np.array(popRanked), columns=["Index","Fitness"])
        df['cum_sum'] = df.Fitness.cumsum()
        df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()
        
        #we compare a randomly drawn number to these weights to select our mating pool
        for i in range(0, len(popRanked) - eliteSize):
            pick = 100*random.random()
            for i in range(0, len(popRanked)):
                if pick <= df.iat[i,3]:
                    selectionResults.append(popRanked[i][0])
                    break 
                
    elif selectionNrUsed == 2: # Turnierbasierte Selektion statt fitnessproportionaler Selektion
        tournamentSize = 2
        tournament_pop = popRanked[eliteSize:]
        while len(selectionResults) < len(popRanked):
            if len(tournament_pop) < tournamentSize:
                tournamentSize = len(tournament_pop)
            
            tournament = random.sample(tournament_pop, tournamentSize)
            tournament = sorted(tournament, key=lambda x: x[1], reverse=True)
            selectionResults.append(tournament[0][0])
            tournament_pop.remove(tournament[0])
        
    elif selectionNrUsed == 3: #TODO: # roulette wheel by calculating a relative fitness weight for each individual
        selectionResults = []
        #TODO
    

    return selectionResults


# why do we repeat almost the same code in this method? 
def selectionWithArchive(popRanked):
    selectionResults = []
    #TODO: Z.B. Turnierbasierte Selektion statt fitnessproportionaler Selektion
    # roulette wheel by calculating a relative fitness weight for each individual
    df = pd.DataFrame(np.array(popRanked), columns=["Index","Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()
    
    #We’ll also want to hold on to our best routes, so we introduce elitism
    #here wie hold all non-dominated solutions
    #TODO: ein festes Archiv vorsehen wie es im ursprünglichen SPEA2 vorgesehen ist 
    for i in range(0, len(popRanked)):
        if (popRanked[i][1] > 1):
            selectionResults.append(popRanked[i][0])
    currentArchiveSize = len(selectionResults)

    #we compare a randomly drawn number to these weights to select our mating pool
    for i in range(0, len(popRanked) - currentArchiveSize):
        pick = 100*random.random()
        for i in range(0, len(popRanked)):
            if pick <= df.iat[i,3]:
                selectionResults.append(popRanked[i][0])
                break
    return selectionResults

def determineNonDominatedArchive(currentGen, popRanked):
    archive = []
    for i in range(0, len(popRanked)):
        if (popRanked[i][1] > 1):
            archive.append(currentGen[popRanked[i][0]])
    #-------Prüfung auf Gleichheit bei Bedarf auskommentieren 
    sameSolutions = []
    for i in range(0, len(archive)-1):
        for j in range(i+1, len(archive)):
            if isSameSolution(archive[i], archive[j]):
                sameSolutions.append(j)
    newArchive = []
    for i in range(0, len(archive)):
        if (not sameSolutions.__contains__(i)):
            newArchive.append(archive[i])
    return newArchive


def determineNonDominatedArchiveSize(popRanked):
    archiveSize = 0
    for i in range(0, len(popRanked)):
        if (popRanked[i][1] > 1):
            archiveSize += 1
    return archiveSize

def isSameSolution(individuumA, individuumB):
    length = len(individuumA)
    i = 0
    isSameSolution = True
    while i < length and isSameSolution:
        if (not (individuumA[i].nr == individuumB[i].nr)):
            isSameSolution = False
            break
        i+=1
    return isSameSolution
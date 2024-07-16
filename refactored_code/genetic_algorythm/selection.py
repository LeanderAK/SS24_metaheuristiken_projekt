import numpy as np, random, operator, pandas as pd

#Create a selection function that will be used to make the list of parent routes
def selection(selectionNrUsed, popRanked, eliteSize):
    selectionResults = []
    
    #Elitism
    for i in range(0, eliteSize):
        selectionResults.append(popRanked[i][0])

    #Turnierbasierte Selektion
    if selectionNrUsed == 2:
        tournamentSize = 2
        tournament_pop = popRanked[eliteSize:]
        while len(selectionResults) < len(popRanked):
            if len(tournament_pop) < tournamentSize:
                tournamentSize = len(tournament_pop)
            
            tournament = random.sample(tournament_pop, tournamentSize)
            tournament = sorted(tournament, key=lambda x: x[1], reverse=True)
            selectionResults.append(tournament[0][0])
            tournament_pop.remove(tournament[0])

    elif selectionNrUsed == 1:
        # Fitnessproportionale skala
        # roulette wheel by calculating a relative fitness weight for each individual
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

    return selectionResults

def selectionWithArchive(selectionNrUsed, archiveRanked):
    selectionResults = []
    # Binäre Turnierbasierte selektion (Ohne elitismus)
    if selectionNrUsed == 2:
        tournamentSize = 2
        tournament_pop = archiveRanked
        while len(selectionResults) < len(archiveRanked):
            if len(tournament_pop) < tournamentSize:
                tournamentSize = len(tournament_pop)
            
            tournament = random.sample(tournament_pop, tournamentSize)
            tournament = sorted(tournament, key=lambda x: x[1], reverse=True)
            selectionResults.append(tournament[0][0])
            tournament_pop.remove(tournament[0])

    return selectionResults

def determineNonDominatedArchive(currentGen, popRanked):
    archive = []
    for i in range(0, len(popRanked)):
        if (popRanked[i][1] > 1):
            archive.append(currentGen[popRanked[i][0]])
    #-------Prüfung auf Gleichheit bei Bedarf auskommentieren 
    # sameSolutions = []
    # for i in range(0, len(archive)-1):
    #     for j in range(i+1, len(archive)):
    #         if isSameSolution(archive[i], archive[j]):
    #             sameSolutions.append(j)
    # newArchive = []
    # for i in range(0, len(archive)):
    #     if (not sameSolutions.__contains__(i)):
    #         newArchive.append(archive[i])
    return archive


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
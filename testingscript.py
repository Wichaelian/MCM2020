import numpy as np
import pandas as pd
from weighted_fairness_functions import runsite, gini
import random

schedule = np.load('schedule.npy')

def testschedule(schedule):
    
    df = pd.read_csv('sites.csv') #read the data from the csv as a pandas dataframe
    dists = np.load('dists.npy')
    stdevs = np.array((df['StDev(Demand per Visit)']))
    variance = stdevs**2
    stdevs = np.sqrt(np.matmul(variance,dists))
    demands = np.array((df['Average Demand per Visit']))
    increment = np.matmul(demands/28, dists) #how much demand increases every day
    
    ntrials = 10
    
    avgfairness = np.zeros(ntrials)
    avgdemand = np.zeros(ntrials)
    ginicoeff = np.zeros(ntrials)
    for i in range(ntrials):
        nsrvd = 0
        fairness = 0
        excessdemand = 0
        nvisits = np.zeros(70)
        for day in schedule:    
            site1 = day[0]
            site2 = day[1]
            
            demand1 = random.normalvariate(demands[site1],stdevs[site1])
            demand2 = random.normalvariate(demands[site2],stdevs[site2])
            
            fair1, nsrvd1 = runsite(demand1)
            fair2, nsrvd2 = runsite(demand2)
            
            fairness += fair1*nsrvd1 + fair2*nsrvd2
            nsrvd += nsrvd1 + nsrvd2
            
            demands = (demands - min(demand1,nsrvd1)*dists[site1])
            demands = (demands - min(demand2,nsrvd2)*dists[site2])
        
            nvisits[site1] += 1
            nvisits[site2] += 1
        
            demands = [0 if x<0 else x for x in demands]
            demands = demands + increment
            excessdemand += sum(demands)
            
        nvisits.sort()
        
        avgdemand[i] = excessdemand/365
        avgfairness[i] = fairness/nsrvd
        ginicoeff[i] = gini(nvisits)
    
    Average_Demand = np.mean(avgdemand)
    Average_Fairness = np.mean(avgfairness)
    Gini_Coefficient = np.mean(ginicoeff)
    
    print('Average Demand: ', Average_Demand)
    print('Average Fairness: ', Average_Fairness)
    print('Gini Coefficient: ', Gini_Coefficient)
    
    return [Average_Demand, Average_Fairness, Gini_Coefficient]

results = testschedule(schedule)
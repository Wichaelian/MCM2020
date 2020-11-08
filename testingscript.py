import numpy as np
import pandas as pd
from weighted_fairness_functions import runsite, gini, returndata
import random

schedule = np.load('schedule.npy')
def testschedule(schedule):
    
    df = pd.read_csv('sites.csv') #read the data from the csv as a pandas dataframe
    dists = np.load('dists.npy')
    data = [df,dists]
    
    demands, stdevs, increment = returndata(data)
    ntrials = 2
    
    avgfairness = np.zeros(ntrials)
    avgdemand = np.zeros(ntrials)
    ginicoeff = np.zeros(ntrials)
    totalfood = np.zeros(ntrials)
    for i in range(ntrials):
        nsrvd = 0
        fairness = 0
        excessdemand = 0
        totallbs = 0
        nvisits = np.zeros(70)
        for day in schedule:    
            site1 = day[0]
            site2 = day[1]
            
            fair1, nsrvd1, lbs1 = runsite(site1, data)
            fair2, nsrvd2, lbs2 = runsite(site2, data)
            
            fairness += fair1*nsrvd1 + fair2*nsrvd2
            nsrvd += nsrvd1 + nsrvd2
            
            demands = (demands - min(254, lbs1/59.08)*dists[site1])
            demands = (demands - min(254, lbs2/59.08)*dists[site2])
            
            #print(demands)
            nvisits[site1] += 1
            nvisits[site2] += 1
        
            demands = [0 if x<0 else x for x in demands]
            demands = demands + increment
            excessdemand += sum(demands)
            totallbs += lbs1+lbs2
            
        nvisits.sort()
        
        avgdemand[i] = excessdemand/365
        avgfairness[i] = fairness/nsrvd
        ginicoeff[i] = gini(nvisits)
        totalfood[i] = totallbs
    
    Average_Demand = np.mean(avgdemand)
    Average_Fairness = np.mean(avgfairness)
    Total_Food = np.mean(totallbs)
    Gini_Coefficient = gini(nvisits)

    print('Average Demand: ', Average_Demand)
    print('Average Fairness: ', Average_Fairness)
    print('Total Food Distributed', Total_Food)
    
    return [Average_Demand, Average_Fairness, Gini_Coefficient]

results = testschedule(schedule)
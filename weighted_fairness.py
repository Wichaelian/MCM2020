import numpy as np
import pandas as pd
from copy import deepcopy
import random
df = pd.read_csv('sites.csv') #read the data from the csv as a pandas dataframe
dists = np.load('dists.npy')

DETERMINISTIC = False

def Fair(quant_demanded):
    if len(quant_demanded) == 0:
        return 0
    
    num = sum(quant_demanded)**2
    denom = len(quant_demanded)*sum([i*i for i in quant_demanded])

    # print("DEBUG:" + " len is "+ str(len(quant_demanded)))
    # print("DEBUG:" + "sum of sqs is " + str(sum([i*i for i in quant_demanded])))
    return num/denom

def runsite(demand):
    demand = int(demand)
    ppl_food_quantity = []      # initialize array of X_i's for ppl's quanitity in lbs for 2 weeks
    if DETERMINISTIC:
        kids = int(round(.41*demand))
        adults = int(round(.4*demand))
        seniors = demand - kids - adults
        ppl_food_quantity = [70]*kids + [56]*adults + [42]*seniors    

    for i in range(0,demand):  # for each person at a site
        if sum(ppl_food_quantity)>15000:
            ppl_food_quantity.append(0)
        else:
            x = random.random()
            if x<= 0.41:     # the person is a child
                ppl_food_quantity.append(5*14)         # 5 lbs of food per day
            elif x <= 0.81:       # the person is an adult
                ppl_food_quantity.append(4*14)         # 4lbs of food a day
            else:                    # the person is a senior
                ppl_food_quantity.append(3*14)       # 3lbs of food a day
    # quantitative meansurement of fairness
    fairness_val = Fair(ppl_food_quantity)

    if 0 not in ppl_food_quantity:
        max_ppl_srvd = demand
    else:
        max_ppl_srvd = ppl_food_quantity.index(0)
    return fairness_val, max_ppl_srvd


stdevs = np.array((df['StDev(Demand per Visit)']))
variance = stdevs**2
stdevs = np.sqrt(np.matmul(variance,dists))
demands = np.array((df['Average Demand per Visit']))
increment = np.matmul(demands/28, dists) #how much demand increases every day
schedules = []
demandDist = []
fairnesslevels = []

nvisits = np.zeros(70)

factorincrements = 10
maxfactor = 20
inc = maxfactor/factorincrements
factor = 0

if DETERMINISTIC:
    ntrials = 1
else:
    ntrials = 2

while factor <= maxfactor:
    print(factor)
    totalexcess = 0

    thislevelschedules = []
    
    for k in range(ntrials):
        optimal = [] #empty list for schedule

        demands = np.array((df['Average Demand per Visit']))
        daysElapsed = [0] * 70
        optimal = []
        excessdemand = 0
        isFair = []
        for day in range(365):

            fx = [factor*x for x in daysElapsed]

            demands = demands + fx
            a = deepcopy(demands)
            a = np.sort(a)

            first = a[-1]
            index1 = np.where(demands == first)

            second = a[-2]
            index2 = np.where(demands == second)

            demands = demands - fx
            
            if DETERMINISTIC:
                demand1 = demands[index1]
                demand2 = demands[index2]
            else:
                demand1 = random.normalvariate(demands[index1],stdevs[index1])
                demand2 = random.normalvariate(demands[index2],stdevs[index2])
                demand1 = max(0,demand1)
                demand2 = max(0,demand2)
                
            fair1, maxsrvd1 = runsite(demand1)
            fair2, maxsrvd2 = runsite(demand2)

            isFair.append(fair1)
            isFair.append(fair2)
            
            demands = (demands - min(demand1,maxsrvd1)*dists[index1])[0]
            demands = (demands - min(demand2,maxsrvd2)*dists[index2])[0]

            daysElapsed = [i + 1 for i in daysElapsed]
            daysElapsed[int(index1[0])] = 0
            daysElapsed[int(index2[0])] = 0

            optimal.append([int(index1[0]),int(index2[0])])
            nvisits[index1] += 1
            nvisits[index2] += 1

            demands = [0 if x<0 else x for x in demands]
            demands = demands + increment
            excessdemand += sum(demands)

        totalexcess += excessdemand
        thislevelschedules.append(optimal)
        fairness = sum(isFair)
        
    schedules.append(thislevelschedules)
    fairnesslevels.append(fairness)
    demandDist.append(totalexcess/(365*ntrials))
    
    factor += inc

print(demandDist)
print(fairnesslevels)

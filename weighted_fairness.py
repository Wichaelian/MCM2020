import numpy as np
import pandas as pd
from copy import deepcopy
import random
df = pd.read_csv('sites.csv') #read the data from the csv as a pandas dataframe
dists = np.load('dists.npy')


def Fair(quant_demanded):
    num = sum(quant_demanded)**2
    denom = len(quant_demanded)*sum([i*i for i in quant_demanded])

    # print("DEBUG:" + " len is "+ str(len(quant_demanded)))
    # print("DEBUG:" + "sum of sqs is " + str(sum([i*i for i in quant_demanded])))
    return num/denom


stdevs = np.array((df['StDev(Demand per Visit)']))
variance = stdevs**2
stdevs = np.sqrt(np.matmul(variance,dists))
demands = np.array((df['Average Demand per Visit']))
#demandtable = np.array(demands)
increment = np.matmul(demands/28, dists) #how much demand increases every day
schedules = []
demandDist = []

nvisits = np.zeros(70)

factorincrements = 50
maxfactor = 5
inc = maxfactor/factorincrements
ntrials = 2

factor = 0

while factor < maxfactor:
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

            demand1 = random.normalvariate(demands[index1],stdevs[index1])
            demand2 = random.normalvariate(demands[index2],stdevs[index2])
            # print(demand1)
            ppl_food_quantity1 = []      # initialize array of X_i's for ppl's quanitity in lbs for 2 weeks
            for i in range(0,int(demand1)):  # for each person at a site
                if sum(ppl_food_quantity1)>15000:
                    ppl_food_quantity1.append(0)
                else:
                    x = random.random()
                    if x<= 0.41:     # the person is a child
                        ppl_food_quantity1.append(5*14)         # 5 lbs of food per day
                    elif x <= 0.81:       # the person is an adult
                        ppl_food_quantity1.append(4*14)         # 4lbs of food a day
                    else:                    # the person is a senior
                        ppl_food_quantity1.append(3*14)       # 3lbs of food a day
            # quantitative meansurement of fairness
            fairness_val1 = Fair(ppl_food_quantity1)

            isFair.append(fairness_val1)
            if 0 not in ppl_food_quantity1:
                max_ppl_srvd1 = demand1
            else:
                max_ppl_srvd1 = ppl_food_quantity1.index(0)
            # print(demand2)
            ppl_food_quantity2 = []
            for j in range(0,int(demand2)):
                if sum(ppl_food_quantity2)>15000:
                    ppl_food_quantity2.append(0)        # for each person at a site
                else:
                    y = random.random()
                    if y <= 0.4:     # the person is a child
                        ppl_food_quantity2.append(5*14)         # 5 lbs of food per day
                    elif y <= 0.81:       # the person is an adult
                        ppl_food_quantity2.append(4*14)         # 4lbs of food a day
                    else:                    # the person is a senior
                        ppl_food_quantity2.append(3*14)     # 3lbs of food a day
            # quantitative meansurement of fairness
            fairness_val2 = Fair(ppl_food_quantity2)
            # print("DEBUG: fairness is ",fairness_val2)
            isFair.append(fairness_val2)
            if 0 not in ppl_food_quantity2:
                max_ppl_srvd2 = demand2
            else:
                max_ppl_srvd2 = ppl_food_quantity2.index(0)

            demands = (demands - min(demand1,max_ppl_srvd1)*dists[index1])[0]
            demands = (demands - min(demand2,max_ppl_srvd2)*dists[index2])[0]

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

    schedules.append(thislevelschedules)
    demandDist.append(totalexcess/(365*ntrials))
    factor += inc
demandDist

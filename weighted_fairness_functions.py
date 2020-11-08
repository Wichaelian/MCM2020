import numpy as np
import random


def Fair(distribution, agegroups):
    allocations = {0:70, 1:56, 2:42}
    if len(distribution) == 0:
        return 0
    
    totalsupply = sum(distribution)
    
    fairscore = 0
    for i in range(len(distribution)):
        recieved = distribution[i]/totalsupply
        allocated = allocations[agegroups[i]]/totalsupply
        fairscore += (recieved-allocated)**2
    
    fairscore = 1/(len(distribution)*fairscore+1)
    # print("DEBUG:" + " len is "+ str(len(quant_demanded)))

    # print("DEBUG:" + "sum of sqs is " + str(sum([i*i for i in quant_demanded])))
    #print(fairscore,totalsupply)
    #print(distribution)
    return fairscore
def runsite(demand, expdemand):
    daysoffood = 14
    ages = np.array([.41,.4,.19])
    fooddist = np.array([5,4,3])   
    evfood = np.dot(ages,fooddist*daysoffood)
    
    demand = int(demand)
    ppl_food_quantity = []      # initialize array of X_i's for ppl's quanitity in lbs for 2 weeks
    agegroups = []
    
    for i in range(0,demand):  # for each person at a site
        expleft = max(int(expdemand*(1-(i/demand))),1)
        foodleft = 15000-sum(ppl_food_quantity)
        expfoodperperson = foodleft/expleft
        ratio = 1

        if expfoodperperson > 70:
            ratio = expfoodperperson/evfood
        elif expfoodperperson < 50:
            ratio = expfoodperperson/evfood
            
        if expfoodperperson<1:
            pass
        x = random.random()
        
        if sum(ppl_food_quantity)>15000:
            ppl_food_quantity.append(0)
            if x<=ages[0]:
                agegroups.append(0)
            elif x<=ages[0]+ages[1]:
                agegroups.append(1)
            else:
                agegroups.append(2)
        else:
            if x<=ages[0]:     # the person is a child
                ppl_food_quantity.append(min(100,max(25,fooddist[0]*daysoffood*ratio)))         # 5 lbs of food per day
                agegroups.append(0)
            elif x <= ages[0]+ages[1]:       # the person is an adult
                ppl_food_quantity.append(min(125,max(25,fooddist[1]*daysoffood*ratio)))         # 4lbs of food a day
                agegroups.append(1)
            else:                    # the person is a senior
                ppl_food_quantity.append(min(80,max(25,fooddist[2]*daysoffood*ratio)))       # 3lbs of food a day
                agegroups.append(2)
    # quantitative meansurement of fairness
    fairness_val = Fair(ppl_food_quantity, agegroups)

    if 0 not in ppl_food_quantity:
        max_ppl_srvd = demand
    else:
        max_ppl_srvd = ppl_food_quantity.index(0)
        
    return fairness_val, max_ppl_srvd, sum(ppl_food_quantity)

def gini(list):
    ## first sort
    arr = np.array(list)
    sorted_arr = arr.copy()
    sorted_arr.sort()
    n = arr.size
    coef_ = 2. / n
    const_ = (n + 1.) / n
    weighted_sum = sum([(i+1)*yi for i, yi in enumerate(sorted_arr)])
    return coef_*weighted_sum/(sorted_arr.sum()) - const_


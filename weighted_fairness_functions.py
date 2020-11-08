import numpy as np
import random


def Fair(distribution, agegroups):
    #adapted the fairness formula to take into account that kids/adults/seniors
    #get different amounts of food by design
    allocations = {0:70, 1:56, 2:42} #0 is kids, 1 is adults, 2 is seniors. 
    if len(distribution) == 0:
        return 0
    
    totalsupply = sum(distribution)
    
    fairscore = 0
    for i in range(len(distribution)):
        recieved = distribution[i]/totalsupply
        allocated = allocations[agegroups[i]]/totalsupply
        fairscore += (recieved-allocated)**2
    
    fairscore = 1/(len(distribution)*fairscore+1)

    return fairscore

def returndata(data):
    df = data[0]
    dists = data[1]
    
    stdevs = np.array((df['StDev(Demand per Visit)']))
    variance = stdevs**2
    stdevs = np.sqrt(np.matmul(variance,dists))
    demands = np.array((df['Average Demand per Visit']))
    increment = np.matmul(demands/(70/772*365), dists) 
    
    return demands, stdevs, increment

def runsite(site, data):
    demands, stdevs, na = returndata(data) #gives the data we need    
    expdemand = demands[site]#expected demand for this site
    stdev = stdevs[site]#standard deviation of demand at this site
    #normally distributed random variable   
    demand = int(random.normalvariate(expdemand,stdev))  
    
    daysoffood = 14 #how many days we expect the food to last everyone
    ages = np.array([.41,.4,.19]) #proportions of kids/adults/seniors
    fooddist = np.array([5,4,3]) #how many lbs of food kids/ad/sen eat each day
    evfood = np.dot(ages,fooddist*daysoffood) #expected value of food demanded by random person
    
    totalfood = min(15000,(expdemand+1.645*stdev)*evfood)
    #bring enough food so that you have >50 pounds per person 95% of the time
    
    ppl_food_quantity = []      # initialize array of X_i's for ppl's quanitity in lbs for 2 weeks
    agegroups = [] #age breakdown of crowd
    
    for i in range(0,demand):  # for each person at a site
        expleft = max(int(expdemand*(1-(i/demand))),1) #expected remaining people
        foodleft = totalfood-sum(ppl_food_quantity) #remaining food
        expfoodperperson = foodleft/expleft #expected remaining food/person
        
        ratio = 1 #default is don't change anything        
        if expfoodperperson > evfood+10: #if we have a lot more food than we expect
            ratio = expfoodperperson/evfood #ratio>1
        elif expfoodperperson < evfood-10: #if we have a lot less food than we expect
            ratio = expfoodperperson/evfood #ratio < 1
            
        x = random.random()#random number to decide age of person
        if x<=ages[0]: #record their age group
                agegroups.append(0)
        elif x<=ages[0]+ages[1]:
            agegroups.append(1)
        else:
            agegroups.append(2)
            
        if sum(ppl_food_quantity)>totalfood: #if were out of food
            ppl_food_quantity.append(0) #you dont get any
        else:
            if x<=ages[0]:     # the person is a child
                ppl_food_quantity.append(min(100,max(35,fooddist[0]*daysoffood*ratio)))         # 5 lbs of food per day
                agegroups.append(0)
            elif x <= ages[0]+ages[1]:       # the person is an adult
                ppl_food_quantity.append(min(125,max(28,fooddist[1]*daysoffood*ratio)))         # 4lbs of food a day
                agegroups.append(1)
            else:                    # the person is a senior
                ppl_food_quantity.append(min(80,max(21,fooddist[2]*daysoffood*ratio)))       # 3lbs of food a day
                agegroups.append(2)
    # quantitative meansurement of fairness
    fairness_val = Fair(ppl_food_quantity, agegroups)

    if 0 not in ppl_food_quantity: #
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


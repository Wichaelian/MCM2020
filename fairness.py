import numpy as np
import pandas as pd
from copy import deepcopy 
import random

df = pd.read_csv('sites.csv') #read the data from the csv as a pandas dataframe
dists = np.load('dists.npy')
stdevs = np.array((df['StDev(Demand per Visit)']))
variance = stdevs**2
stdevs = np.sqrt(np.matmul(variance,dists))

for gap in range(8,36):
    maxgap = gap*5 #the maximum number of days between site visits
    route = []
    demands = np.array((df['Average Demand per Visit'])) 
    increment = np.matmul(demands/(365/(722/70)),dists)
    
    excessdemand = 0       #cumulative unfulfilled demand
    nvisits = np.zeros(70) #how often each site is visited - starts at 0
    
    dayssince = np.zeros(70) #days since the last site visit
    
    for day in range(365):
        a = deepcopy(demands)#sort a copy of the demands array
        a = np.sort(a) 
        
        b = deepcopy(dayssince)
        b = np.sort(b)
        
        revisit = False
        for i in range(len(b)):
            if maxgap-b[i]<35-i/2:
                revisit = True
        
        if not revisit:
            #last and 2nd to last elements in sorted array are the highest and second highest elements
            first = a[-1]
            second = a[-2]
            
            #index of 1st & 2nd highest elements
            index1 = np.where(demands == first) 
            index2 = np.where(demands == second)
        elif revisit:
            index1 = np.where(dayssince == b[-1])[0]
            index2 = np.where(dayssince == b[-2])[0]
            if type(index1) == np.ndarray:
                index1 = index1[:1]
            if type(index2) == np.ndarray:
                index2 = index2[-1:]
                
        firstsite = random.normalvariate(demands[index1],stdevs[index1])
        secondsite = random.normalvariate(demands[index2],stdevs[index2])
        
        #the amount that demand changes due to visiting the two sites
        demands = (demands - min(firstsite,300)*dists[index1])[0]
        demands = (demands - min(secondsite,300)*dists[index2])[0]
        #food can be distributed to a maximum of 300 people at each site    
    
        for i in range(len(demands)):
            if demands[i]<0:
                demands[i] = 0
        
        #keep track of the visited sites 
        route.append([index1,index2])
        nvisits[index1] += 1
        nvisits[index2] +=1
        dayssince[index1] = 0
        dayssince[index2] = 0
        dayssince = dayssince + 1
        
        demands = demands + increment #each day demand increases by the same increment
        excessdemand += sum(demands) #total amount of hunger out there?
        
    print("Average Outstanding Demand: ", excessdemand/365) #average amount of hunger?
    print('Visit disparity: ',np.std(nvisits))
    print('Gap: ',gap*5)
    #print("Number of visits to each site: ", nvisits) #number of visits to each site
    #print(optimal) #the determined schedule 
        
        
    #

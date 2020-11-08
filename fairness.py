import numpy as np
import pandas as pd
from copy import deepcopy 
import random

df = pd.read_csv('sites.csv') #read the data from the csv as a pandas dataframe
dists = np.load('dists.npy')
stdevs = np.array((df['StDev(Demand per Visit)']))
variance = stdevs**2
stdevs = np.sqrt(np.matmul(variance,dists))

route = []
demands = np.array((df['Average Demand per Visit'])) 
increment = np.matmul(demands/(365/(722/70)),dists)
    
excessdemand = 0       #cumulative unfulfilled demand
nvisits = np.zeros(70) #how often each site is visited - starts at 0

for day in range(365):
     a = deepcopy(demands)#sort a copy of the demands array
     a = np.sort(a) 
     
   
     first = a[-1]
     second = a[-2]
    
     #index of 1st & 2nd highest elements
     index1 = np.where(demands == first) 
     index2 = np.where(demands == second)
     
     firstsite = demands[index1][0]
     secondsite = demands[index2][0]
     
     #the amount that demand changes due to visiting the two sites
     demands = (demands - min(firstsite,300)*dists[index1])[0]
     demands = (demands - min(secondsite,300)*dists[index2])[0]
     #food can be distributed to a maximum of 300 people at each site    
 
     for i in range(len(demands)):
         if demands[i]<0:
             demands[i] = 0
     
     #keep track of the visited sites 
     route.append([index1[0][0],index2[0][0]])
     nvisits[index1] += 1
     nvisits[index2] +=1
     
     demands = demands + increment #each day demand increases by the same increment
     excessdemand += sum(demands) #total amount of hunger out there?
     
print("Average Outstanding Demand: ", excessdemand/365) #average amount of hunger?
print('Visit disparity: ',np.std(nvisits))
#print("Number of visits to each site: ", nvisits) #number of visits to each site
print(route) #the determined schedule 
     
     
 #

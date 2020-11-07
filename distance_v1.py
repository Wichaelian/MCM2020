import numpy as np
import pandas as pd
from math import radians, cos, sin, asin, sqrt

df = pd.read_csv('sites.csv')

dists = np.zeros([70,70])

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 3956  # Radius of earth in miles
    return c * r    

for i in range(len(df)):
    s1 = df.iloc[i]
    s1lat = s1['latitude']
    s1long = s1['longitude']
    for j in range(len(df)):
        s2 = df.iloc[j]
        s2lat = s2['latitude']
        s2long = s2['longitude']
        
        dist = haversine(s1long,s1lat,s2long,s2lat)
        
        dists[i,j] = dist

sqrts = np.zeros([70])

for row in range(len(dists)):
    sqrts[row] = (sqrt(np.sum((np.max(dists)-dists[row])**2)))/70
    #sqrt of average of squares of distances

largest_coeff = .75 #most central site will  have .25 weight on own demand, .75 on others

sqrts = (sqrts-min(sqrts))/((max(sqrts))*largest_coeff) #rescaled to go from 0-.75

for row in range(len(dists)):
    thisrow = dists[row]
    weights = sum(thisrow)
    thisrow = thisrow/weights*sqrts[row]
    dists[row] = thisrow

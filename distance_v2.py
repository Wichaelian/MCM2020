import numpy as np
import pandas as pd
from math import radians, cos, sin, asin, sqrt

df = pd.read_csv('sites.csv') #read the data from the csv as a pandas dataframe
dists = np.zeros([70,70]) #create an empty 70x70 array

def haversine(lon1, lat1, lon2, lat2):
    """function to find the distance between two points on earth w/ latitude
    and longitude.
    I found it online which im pretty sure is ok to admit in this class"""

    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 3956  # Radius of earth in miles
    return c*r

for i in range(len(df)): #cycle through all the sites in order to find the
    s1 = df.iloc[i]      #distance between all of them
    s1lat = s1['latitude']
    s1long = s1['longitude']
    for j in range(len(df)):
        s2 = df.iloc[j]
        s2lat = s2['latitude']
        s2long = s2['longitude']

        dist = haversine(s1long,s1lat,s2long,s2lat) #distance between s1 and s2
        dists[i,j] = dist
        #after this loop is complete the dists array will be full, with each
        #element at position (i,j) containing the distance between the ith and
        #jth sites in the dataframe containing all the sites

sqrts = np.zeros([70]) #create an empty array with 70 elements

for row in range(len(df)): #loop over each site
    tenclosest = np.sort(dists[row])[1:11]
    #distances to 10 closest sites from this site (0 is the original site)
    harmean = 10/sum(1/(tenclosest))
    sqrts[row] = harmean
    #set sqrts[row] to the harmonic mean of the ten closest sites
    #this gives us a value that determines how much demand at this site is
    #influenced by demand at nearby sites. The exact values aren't important,
    #just their sizes relative to each other

largest_coeff = .75 #most central site will  have .25 weight on own demand, .75 on others
sqrts = (sqrts-min(sqrts))/(max(sqrts)-min(sqrts))*largest_coeff
sqrts = sqrts
#rescale the values of sqrts to go from 0-.75
#0 means weight actual demand as 1, 0 input from other sites
for row in range(len(dists)): #go through each row in the dists array
    thisrow = dists[row] #distances to each site from this site
    thisrow = max(thisrow)-thisrow #make long distances low and short distances high
    thisrow = thisrow**2 #closest sites have highest weights
    thisrow[row] = 0 #set this site's weight to 0
    totalsum = sum(thisrow)
    thisrow = thisrow/totalsum*sqrts[row] #scale elements in thisrow so that they add to sqrts[row]
    thisrow[row] = 1-sqrts[row] #this site gets all remaning weight
    dists[row] = thisrow #change the dists array


np.save('dists.npy', dists)

# [[65, 1], [16, 2], [27, 31], [12, 61], [10, 30], [29, 21], [65, 28], [5, 68], [4, 9], [64, 67], [0, 66], [63, 8], [69, 20], [15, 33], [25, 7], [3, 17], [62, 1], [13, 22], [26, 14], [16, 32], [65, 2], [18, 23], [27, 31], [61, 12], [10, 34], [11, 21], [29, 30], [6, 19], [28, 24], [39, 4], [5, 64], [67, 68], [65, 1], [0, 9], [63, 16], [33, 20], [2, 66], [69, 8], [25, 61], [31, 27], [17, 3], [12, 7], [10, 22], [15, 65], [14, 21], [29, 13], [30, 62], [1, 32], [28, 23], [26, 18], [4, 64], [16, 5], [34, 2], [67, 11], [68, 65], [0, 61], [27, 31], [9, 63], [12, 42], [10, 19], [33, 20], [41, 6], [1, 66], [24, 25], [8, 69], [21, 17], [29, 65], [30, 3], [16, 56], [7, 39], [28, 2], [22, 64], [4, 14], [5, 15], [31, 61], [27, 13], [67, 12], [1, 68], [65, 57], [62, 0], [10, 32], [23, 9], [18, 26], [63, 36], [52, 16], [21, 33], [20, 34], [2, 29], [30, 11], [66, 51], [65, 46], [25, 8], [69, 28], [1, 31], [27, 61], [17, 64], [12, 4], [3, 5], [7, 19], [10, 53], [22, 67], [68, 16], [6, 14], [65, 24], [0, 15], [2, 9], [21, 13], [63, 29], [1, 30], [39, 31], [33, 23], [62, 61], [27, 32], [20, 28], [12, 18], [65, 26], [66, 64], [10, 4], [16, 25], [8, 69], [5, 34], [42, 17], [11, 2], [67, 3], [1, 41], [68, 7], [21, 0], [65, 22], [31, 29], [30, 9], [61, 27], [14, 56], [12, 63], [43, 19], [15, 16], [28, 10], [13, 33], [64, 6], [24, 20], [1, 2], [65, 4], [57, 5], [66, 23], [62, 32], [25, 18], [8, 69], [31, 21], [67, 17], [27, 26], [61, 29], [68, 30], [12, 0], [3, 16], [65, 36], [39, 7], [9, 1], [10, 34], [11, 22], [2, 28], [63, 64], [14, 52], [33, 4], [46, 5], [31, 20], [15, 65], [27, 51], [21, 13], [61, 16], [66, 12], [29, 19], [1, 30], [67, 25], [8, 69], [23, 68], [10, 17], [2, 0], [62, 32], [65, 6], [24, 18], [28, 3], [9, 47], [42, 26], [31, 64], [7, 63], [27, 4], [16, 22], [1, 61], [5, 12], [21, 33], [41, 50], [65, 20], [29, 14], [30, 34], [2, 11], [58, 53], [10, 15], [67, 66], [40, 56], [68, 39], [13, 25], [8, 0], [69, 31], [1, 65], [27, 16], [28, 17], [61, 35], [9, 64], [12, 23], [4, 19], [21, 3], [32, 62], [63, 5], [2, 18], [29, 57], [30, 7], [65, 10], [33, 22], [26, 20], [1, 24], [6, 31], [16, 67], [14, 27], [68, 37], [66, 36], [0, 61], [12, 28], [15, 34], [25, 65], [8, 11], [69, 2], [64, 21], [9, 13], [4, 49], [17, 44], [1, 29], [10, 5], [30, 63], [16, 3], [31, 23], [27, 46], [65, 39], [33, 32], [7, 62], [61, 20], [12, 67], [18, 52], [22, 42], [68, 2], [28, 19], [0, 55], [1, 66], [26, 14], [21, 64], [65, 51], [41, 10], [16, 25], [4, 29], [8, 9], [31, 30], [27, 69], [15, 5], [6, 24], [17, 34], [63, 61], [12, 11], [43, 13], [2, 65], [1, 56], [3, 38], [67, 33], [59, 28], [7, 20], [68, 23], [16, 21], [10, 0], [62, 22], [32, 64], [31, 27], [66, 29], [65, 4], [30, 18], [61, 57], [9, 1], [14, 12], [2, 5], [25, 39], [8, 26], [69, 19], [45, 63], [48, 53], [16, 17], [65, 54], [15, 28], [10, 67], [21, 36], [31, 27], [3, 33], [68, 13], [1, 20], [0, 34], [29, 64], [7, 61], [30, 24], [2, 6], [12, 11], [4, 65], [66, 22], [23, 9], [5, 16], [62, 32], [42, 25], [18, 14], [10, 63], [27, 8], [31, 1], [28, 69], [21, 46], [65, 67], [17, 41], [26, 61], [2, 29], [68, 12], [64, 33], [30, 0], [15, 3], [16, 20], [19, 4], [47, 50], [39, 52], [13, 65], [1, 7], [5, 27], [10, 31], [9, 56], [66, 34], [22, 58], [40, 28], [21, 2], [61, 25], [63, 11], [23, 51], [12, 8], [65, 67], [29, 32], [62, 16], [69, 30], [24, 14], [6, 1], [68, 64], [18, 17], [0, 27], [4, 33], [31, 10], [20, 26], [3, 57], [65, 5], [2, 15], [61, 9], [21, 7], [28, 12], [16, 13], [66, 35], [1, 22], [63, 29], [19, 36]]

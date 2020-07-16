import matplotlib.pyplot as plt
import time
import numpy as np
a = [0 for i in range(3)]

def from_data_to_ball(pSet,dimension):
    n = len(pSet)
    mean = [0 for i in range(dimension)]
    for i in range(dimension):
        for x in pSet:
            mean[i] += x[1][i]
        mean[i] = mean[i]/n
    
    #mean = [sum(x[1][i] for x in pSet)/n for i in range(dimension)]
    #left_pivot,radius = farthest_point(mean,pSet)
    #right_pivot,_ = farthest_point(left_pivot[1],pSet)
    return mean#, radius#, left_pivot, right_pivot

def from_data_to_ball1(pSet,dimension):
    n = len(pSet)
    '''
    mean = [0 for i in range(dimension)]
    for i in range(dimension):
        for x in pSet:
            mean[i] += x[1][i]
        mean[i] = mean[i]/n
    '''
    mean = [sum(x[1][i] for x in pSet)/n for i in range(dimension)]
    #left_pivot,radius = farthest_point(mean,pSet)
    #right_pivot,_ = farthest_point(left_pivot[1],pSet)
    return mean#, radius#, left_pivot, right_pivot

def from_data_to_ball2(pSet,dimension): 
    cent = np.mean([x[1] for x in pSet],axis=0)
    #left_pivot,radius = farthest_point(mean,pSet)
    #right_pivot,_ = farthest_point(left_pivot[1],pSet)
    return cent #, radius#, left_pivot, right_pivot

pSet = [[1,[0,0]],[1,[1,1]],[3,[2,4]]]
dimension = 2

start = time.time()
for i in range(100000):
    a = from_data_to_ball2(pSet,dimension)
print(a,time.time()-start)


start = time.time()
for i in range(100000):
    a = from_data_to_ball1(pSet,dimension)
print(a,time.time()-start)

start = time.time()
for i in range(100000):
    a = from_data_to_ball(pSet,dimension)
print(a,time.time()-start)

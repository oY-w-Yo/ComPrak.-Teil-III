import numpy as np
#import heapq as hp
import math
from   random import choice
import timeit



######################## Define some useful help functions ###########################

# squre of distance of two pure points
def distance_sq(p1,p2):
    maxi = 0
    for a,b in zip(p1,p2):
        c = abs(a-b)
        if c > maxi:
            maxi = c
    return maxi


def distance_sq2(p1,p2):
    maxi = 0
    for i in range(len(p1)):
        c = p1[i] - p2[i]
        if c > maxi:
            maxi = c
    return maxi

'''
test1 = 'p1 = [10,203,4,55,40];p2 = [20,40,120,40,1];distance_sq(p1,p2)'
test2 = 'p1 = [10,203,4,55,40];p2 = [20,40,120,40,1];distance_sq2(p1,p2)'
print(timeit.timeit(test1,'from __main__ import distance_sq',number=100000))
print(timeit.timeit(test2,'from __main__ import distance_sq2',number=100000))
'''

# d(p,Ball) = d(p,Ball_center) - Ball_radius
# d(p,Ball)^2 = d(p,Ball_center)^2 + Ball_radius^2 - 2*d(p,Ball_center)*Ball_radius, also
# d(p,Ball)_sq = d(p,Ball_center)_sq + Ball_radius_sq 
def distance_sq_Ball(p,Ball_center,Ball_radius_sq):
    k_sq = distance_sq(p,Ball_center)
    r_sq = Ball_radius_sq 
    d_sq = k_sq + r_sq - 2*math.sqrt(k_sq * r_sq)
    return d_sq
 
# special for the datastructure, we have data in form [label, vektor] in pSet
def k_closest_point(Point,pSet,k):
    index_list = range(len(pSet)) 
    distance_set = [distance_sq(p[1],Point) for p in pSet]
    index_list = sorted(index_list, key = lambda i: distance_set[i])[:k]
    #index_list = hp.nsmallest(k,index_list, key = lambda i: distance_set[i])
    return [pSet[i] for i in index_list],[distance_set[i] for i in index_list]

# p is a pure vektor and every point in  pSet is in form [label, vektor]
# the output is also in form [label, vektor]
def farthest_point(p,pSet):
    farthest = pSet[0]
    for q in pSet:
        if distance_sq(p,q[1]) > distance_sq(p,farthest[1]):
            farthest = q
    return farthest

# 1. choose a point p randomly 2. find the point f1, fartherst from p
# 3. find the point f2, fartherst from f1
def greatest_spread(pSet):
    p = choice(pSet)
    f1 = farthest_point(p[1],pSet)
    f2 = farthest_point(f1[1],pSet)
    f = [f1[1][i] - f2[1][i] for i in range(len(f1[1]))]
    return f


def projection(w,p):
    return np.dot(w,p) # this function is here to make the code more readable


def ErrorCal(func,TestSet):
    m = len(TestSet)
    Error = sum(labeled_point[0] != func(labeled_point[1]) for labeled_point in TestSet)
    Error = Error/m
    return Error

def Error(Point,k_best):
    result = sum(p[0] for p in k_best)
    if result < 0:
        result = -1
    else:
        result = 1
    return result != Point[0]

def point_error(Point,sum_label):
    if sum_label < 0:
        result = -1
    else:
        result = 1
    return result != Point[0]

def merge_two_k_best(Set1,distance_set1,Set2,distance_set2,k):
    if Set1 == []:
        return Set2,distance_set2
    #if Set2 == []:
    #    return Set1,distance_set1
    if len(Set1) < k or distance_set2[0] < distance_set1[-1]:
        temp_Best = Set1 + Set2
        temp_distance_set = distance_set1 + distance_set2
        temp_index = range(len(temp_Best))
        temp_index = sorted(temp_index, key = lambda i: temp_distance_set[i])[:k]
        Set1 = [temp_Best[i] for i in temp_index]
        distance_set1 = [temp_distance_set[i] for i in temp_index]
    return Set1,distance_set1

def sgnial(value):
    if value < 0:
        return -1
    else:
        return 1


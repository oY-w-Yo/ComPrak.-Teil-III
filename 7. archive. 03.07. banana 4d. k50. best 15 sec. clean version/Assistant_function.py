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
 
# special for the datastructure, we have data in form [label, vektor] in pSet
def k_closest_point(Point,pSet,k):
    index_list = range(len(pSet)) 
    distance_set = [distance_sq(p[1],Point) for p in pSet]
    index_list = sorted(index_list, key = lambda i: distance_set[i])[:k]
    #index_list = hp.nsmallest(k,index_list, key = lambda i: distance_set[i])
    return [pSet[i] for i in index_list],[distance_set[i] for i in index_list]

def ErrorCal(func,TestSet):
    m = len(TestSet)
    Error = sum(labeled_point[0] != func(labeled_point[1]) for labeled_point in TestSet)
    Error = Error/m
    return Error

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
    if distance_set2[0] < distance_set1[-1]:
        temp_Best = Set1 + Set2
        temp_distance_set = distance_set1 + distance_set2
        temp_index = range(len(temp_Best))
        temp_index = sorted(temp_index, key = lambda i: temp_distance_set[i])[:k]
        Set1 = [temp_Best[i] for i in temp_index]
        distance_set1 = [temp_distance_set[i] for i in temp_index]
    return Set1,distance_set1


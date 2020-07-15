import numpy as np
import math
import copy
from   random import choice,sample
import timeit
from Assistant_class import CallingCounter



######################## Define some useful help functions ###########################

# maximum norm of two pure points
@CallingCounter
def distance_max(p1,p2):
    maxi = 0
    for a,b in zip(p1,p2):
        c = abs(a-b)
        if c > maxi:
            maxi = c
    return maxi

def distance_max_Ball(p,Ball_center,Ball_radius):
    #return 10
    return distance_max(p,Ball_center) - Ball_radius
 
# special for the datastructure, we have data in form [label, vektor] in pSet
@CallingCounter
def k_closest_point(Point,pSet,k):
    index_list = range(len(pSet)) 
    distance_set = [distance_max(p[1],Point) for p in pSet]
    index_list = sorted(index_list, key = lambda i: distance_set[i])[:k]
    #index_list = hp.nsmallest(k,index_list, key = lambda i: distance_set[i])
    return [pSet[i] for i in index_list],[distance_set[i] for i in index_list]

# p is a pure vektor and every point in  pSet is in form [label, vektor]
# the output is also in form [label, vektor]
def farthest_point(p,pSet):
    farthest = pSet[0]
    distance_farthest = distance_max(p,farthest[1])
    for q in pSet:
        distance_temp = distance_max(p,q[1])
        if distance_temp > distance_farthest:
            distance_farthest = distance_temp
            farthest = q
    return farthest, distance_farthest

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

def axis_find(pSet,dimension):
    pSet_sort = []
    width = 0
    d = 0
    for i in range(dimension):
        pSet_temp_sort = sorted(pSet,key=lambda p: p[1][i])
        width_temp = pSet_temp_sort[-1][1][i] - pSet_temp_sort[0][1][i]
        if width_temp > width:
            width = width_temp
            pSet_sort = pSet_temp_sort
            d = i
    
    return pSet_sort,d

def direction_find(pSet,dimension):
    #pSet_sort = []
    #direction = None
    p = choice(pSet)
    f1,_ = farthest_point(p[1],pSet)
    f2,_ = farthest_point(f1[1],pSet)
    direction = [f1[1][i] - f2[1][i] for i in range(dimension)]
    direction = direction/np.linalg.norm(direction)
    pSet_sort = sorted(pSet,key=lambda p: np.dot(p[1],direction))
    return pSet_sort,direction

def direction_find1(pSet,dimension,leafsize):
    # choose leafsize points in pSet randomly
    if len(pSet) > leafsize:
        pSet_sample = sample(pSet,leafsize)
    else:
        pSet_sample = pSet
    #direction = None
    p = choice(pSet_sample)
    f1,_ = farthest_point(p[1],pSet_sample)
    f2,_ = farthest_point(f1[1],pSet_sample)
    direction = [f1[1][i] - f2[1][i] for i in range(dimension)]
    pSet_sort = sorted(pSet,key=lambda p: np.dot(p[1],direction))
    return pSet_sort,direction

def Test(func,Testset):
    Error_result = 0
    temp_test = copy.deepcopy(Testset)
    for x in temp_test: # x in form [Label, Vector]
        #x.append(func(x[1]))  # x in form [Label, Vector, Output_label]
        y = func(x[1])
        print('f({})={}'.format(x[1],y))
        x.extend(y) # x in form [Label, Vector, Output_label, k_star_best_list]
        if x[0] != x[2]:
            Error_result += 1
    average_Error = float(Error_result/len(temp_test))
    #print("testset",temp_test)
    return temp_test,average_Error
import numpy as np
import heapq as hp
import math
import copy
from   random import choice,sample
import timeit
from Assistant_class import CallingCounter



######################## Define some useful help functions ###########################

# maximum norm of two pure points
#@CallingCounter
def distance_max(p1,p2):
    maxi = 0
    for a,b in zip(p1,p2):
        c = abs(a-b)
        if c > maxi:
            maxi = c
    return maxi

def distance_sq_Ball(p,Ball_center,Ball_radius):
    return distance_max(p,Ball_center) - Ball_radius
 
# special for the datastructure, we have data in form [label, vektor] in pSet
#@CallingCounter
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

def from_data_to_ball(pSet,dimension):
    p = choice(pSet)
    f1,_ = farthest_point(p[1],pSet)
    f2,_ = farthest_point(f1[1],pSet)
    crentrum = [(f1[1][i] + f2[1][i])/2 for i in range(dimension)]
    left_pivot,radius = farthest_point(crentrum,pSet)
    right_pivot,_ = farthest_point(left_pivot[1],pSet)
    return crentrum, radius, left_pivot, right_pivot



# 1. choose a point p randomly 2. find the point f1, fartherst from p
# 3. find the point f2, fartherst from f1
def greatest_spread(pSet):
    p = choice(pSet)
    f1 = farthest_point(p[1],pSet)
    f2 = farthest_point(f1[1],pSet)
    f = [f1[1][i] - f2[1][i] for i in range(len(f1[1]))]
    return f


def projection(w,p):
    return sum(w[i]*p[i] for i in range(len(w))) # this function is here to make the code more readable


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

#@CallingCounter
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
    n = len(pSet)
    p = choice(pSet)
    f1,_ = farthest_point(p[1],pSet)
    f2,_ = farthest_point(f1[1],pSet)
    direction = [f1[1][i] - f2[1][i] for i in range(dimension)]
    project = [projection(p[1],direction) for p in pSet]
    index = range(len(project))
    index = sorted(index, key= lambda i: project[i])
    #pSet_sort = sorted(pSet,key=lambda p: projection(p[1],direction))
    pSet_sort = [pSet[i] for i in index]
    pivot = pSet_sort[int(n/2)]
    pivot_project = project[int(n/2)]
    return pSet_sort,direction,pivot,pivot_project

'''
def direction_find1(pSet,pivot,radius,dimension):
    n = len(pSet)
    if pivot == None:
        direction = np.zeros(dimension)
        sorted_points,axis = axis_find(pSet,dimension)
        dimension[axis] = 1
        pivot = sorted_points[int(n/2)]
        LeftSet  = sorted_points[:int(n/2)]
        RightSet = sorted_points[int(n/2):]
    else:
        LeftSet = []
        RightSet = []
        f1,_ = farthest_point(pivot[1],pSet)
        f2,_ = farthest_point(f1[1],pSet)
        direction = [f1[1][i] - f2[1][i] for i in range(dimension)]
        for x in pSet:
            pass
    return pSet_sort,direction
'''

def Test1(func,Testset):
    Error_result = 0
    temp_test = copy.deepcopy(Testset)
    for x in temp_test: # x in form [Label, Vector]
        #x.append(func(x[1]))  # x in form [Label, Vector, Output_label]
        x.extend(func(x[1])) # x in form [Label, Vector, Output_label, k_star_best_list]
        if x[0] != x[2]:
            Error_result += 1
    average_Error = float(Error_result/len(temp_test))
    #print(temp_test,'\n')
    return temp_test,average_Error

def Test(func,Testset):
    Error_result = 0
    result = []
    for x in Testset: # x in form [Label, Vector]
        y = func(x[1])
        result.append([x[0],x[1],y[0],y[1]])
        #x.append(func(x[1]))  # x in form [Label, Vector, Output_label]
        #x.extend(func(x[1])) # x in form [Label, Vector, Output_label, k_star_best_list]
        if x[0] != y[0]:
            Error_result += 1
    average_Error = float(Error_result/len(Testset))
    #print(temp_test,'\n')
    return result,average_Error
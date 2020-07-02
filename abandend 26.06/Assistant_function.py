import numpy as np
import math
from random import choice
import timeit
import copy
######################## Define some useful help functions ###########################

# squre of distance of two pure points
def distance_sq(p1,p2):
    d = 0
    for a,b in zip(p1,p2):
        c = abs(a-b)
        if c > d:
            d = c
    return d

def test_dis():
    test1 = 'p1 = [10,203,4,55,40,1,2,3,4,5,10,203,4,55,40,1,2,3,4,5];p2 = [20,40,120,40,1,3,4,5,6,7,10,203,4,55,40,1,2,3,4,5];distance_sq1(p1,p2)'
    test2 = 'p1 = [10,203,4,55,40,1,2,3,4,5,10,203,4,55,40,1,2,3,4,5];p2 = [20,40,120,40,1,3,4,5,6,7,10,203,4,55,40,1,2,3,4,5];distance_sq2(p1,p2)'
    #test3 = 'p1 = [10,203,4,55,40,1,2,3,4,5,10,203,4,55,40,1,2,3,4,5];p2 = [20,40,120,40,1,3,4,5,6,7,10,203,4,55,40,1,2,3,4,5];distance_sq3(p1,p2)'
    print(timeit.timeit(test1,'from __main__ import distance_sq1',number=100000))
    print(timeit.timeit(test2,'from __main__ import distance_sq2',number=100000))
    #print(timeit.timeit(test3,'from __main__ import distance_sq3',number=100000))

#test_dis()


# d(p,Ball) = d(p,Ball_center) - Ball_radius
# d(p,Ball)^2 = d(p,Ball_center)^2 + Ball_radius^2 - 2*d(p,Ball_center)*Ball_radius, also
# d(p,Ball)_sq = d(p,Ball_center)_sq + Ball_radius_sq 
def distance_sq_Ball(p,Ball_center,Ball_radius_sq):
    k_sq = distance_sq(p,Ball_center)
    r_sq = Ball_radius_sq 
    d_sq = k_sq + r_sq - 2*math.sqrt(k_sq * r_sq)
    return d_sq
 
# special for the datastructure, we have data in form [label, vektor] in pSet
# Assumed there are no same point
def k_closest_point(Point,pSet,k):
    index_list = range(len(pSet)) 
    distance_set = [distance_sq(pSet[i][1],Point) for i in index_list]
    index_list = sorted(index_list, key = lambda i: distance_set[i])[:k]
    return [pSet[i] for i in index_list],[distance_set[i] for i in index_list]

# special for the datastructure, we have data in form [label, vector] in orderedSet and newpoint
# we assumed that the ordereSet already contain k_closest_point
def insert_into_k_closest_point(p,orderdSet,newpoint):
    d = distance_sq(p,newpoint[1])
    for i in range(len(orderdSet)):
        if d < distance_sq(p,orderdSet[-i][1]):
            orderdSet.insert(-i,newpoint)
            orderdSet.remove(orderdSet[-1])
            break
    return orderdSet

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
    #m = len(TestSet)
    Error = np.mean([labeled_point[0] != func(labeled_point[1]) for labeled_point in TestSet])
    #Error = Error/m
    return Error

# return 1, if 
def Error(Point,k_best):
    result = sum([p[0] for p in k_best])
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


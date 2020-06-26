import numpy as np
import math
from random import choice
######################## Define some useful help functions ###########################

# squre of distance of two pure points
def distance_sq(p1,p2):
    #d = np.dot(np.array(p1)-np.array(p2),np.array(p1)-np.array(p2))
    #d = sum([(p1[i]-p2[i])**2 for i in range(len(p1))])
    d = 0
    for i in range(len(p1)):
        d += (p1[i]-p2[i])**2
    return d

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
    pSet = sorted(pSet, key = lambda p: distance_sq(p[1],Point))
    return pSet[:k]

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
    m = len(TestSet)
    Error = sum([labeled_point[0] != func(labeled_point[1]) for labeled_point in TestSet])
    Error = Error/m
    return Error

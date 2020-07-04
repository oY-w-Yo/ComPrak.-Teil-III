import csv
import math
import time
import numpy as np
from enum import Enum
from random import shuffle
from random import choice


# Read the Data from 
def read_csv(name,Settype):
    File_csv = name + "." + Settype + ".csv"
    with open('classification-artificial/'+File_csv) as File:
        Data = csv.reader(File, delimiter=',')
        pointSet = []
        for point in Data:
            for i in range(len(point)):
                point[i] = float(point[i])
            pointSet.append([ point[0], point[1:] ])
    return pointSet

######################## Define some useful help functions ###########################

# squre of distance of two pure points
def distance_sq(p1,p2):
    n = len(p1)
    d = 0
    for i in range(n):
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
def k_closest_point(p,pSet,k):
    for q in pSet:
        q.append(distance_sq(p,q[1]))
    pSet = sorted(pSet,key = lambda point: point[2])
    for q in pSet:
        q.remove(q[-1])
    return pSet[:k]

# special for the datastructure, we have data in form [label, vektor] in orderedSet and newpoint
def insert_into_k_closest_point(p,orderdSet,newpoint,maxLength):
    d = distance_sq(p,newpoint[1])
    for i in range(len(orderdSet)):
        if d < distance_sq(p,orderdSet[i][1]):
            orderdSet.insert(i,newpoint)
            break
    else:
        orderdSet.append(newpoint)
    
    if len(orderdSet) > maxLength:
        orderdSet.remove(orderdSet[-1])
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


class Ball_Node:
    def __init__(self, Data):
        self.Data = Data
        self.LeftChild = None
        self.RightChild = None
        self.position = None
        self.pivot = None # here is the pivot point also the center point
        self.radius_sq = None
        self.greatest_direction = greatest_spread(Data)
        self.sorted_data = None
        self.creat_Node()
    
    def creat_Node(self):
        Dataset =self.Data
        w = self.greatest_direction
        self.sorted_data = sorted(Dataset,key = lambda point: projection(w,point[1]))
        n = len(self.sorted_data)
        self.pivot = self.sorted_data[int(n/2)]
        p = self.pivot
        self.radius_sq = distance_sq(farthest_point(p[1],Dataset)[1], p[1])


class Position(Enum):
    InsidePoint = 1
    Leaf = 2

# Define the Ball-tree class.
class Ball_Tree:    
    def __init__(self, trainData, trainLabel, leafsize=10, depth=0):
        self.label = trainLabel
        self.depth = depth
        self.root = None
        self.leafsize = leafsize

        if len(trainData) > 0:
            self.d = len(trainData[0][1])
            self.creat_tree(trainData)

    def creat_tree(self,DataSet):
        n = len(DataSet)
        self.root = Ball_Node(DataSet)
        if n <= self.leafsize:
            self.root.position = Position.Leaf
        else:
            self.root.position = Position.InsidePoint
            self.root.LeftChild = Ball_Tree(self.root.sorted_data[:int(n/2)], self.label, self.depth + 1,self.leafsize)
            self.root.RightChild = Ball_Tree(self.root.sorted_data[int(n/2)+1:], self.label, self.depth + 1,self.leafsize)
    
    def print_tree(self):
        if self.root is not None:
            if self.root.position == Position.Leaf:
                print(len(self.root.Data),self.root.Data)
            else:
                print(self.root.pivot)
                if (self.root.LeftChild is not None) and (self.root.RightChild is not None):
                    self.root.LeftChild.print_tree()
                    self.root.RightChild.print_tree()

    def search_k_nearst_in_tree(self, Point, k=1):
        if self.root.position == Position.Leaf:
            if len(self.root.Data) == 0 or self.root == None:
                return None
            else:
                k_Best = k_closest_point(Point,self.root.Data,k)
                return k_Best
        
        next_Brunch = None
        oppesite_Brunch = None
        w = self.root.greatest_direction
        if  projection(w,Point)< projection(w,self.root.pivot[1]):
            next_Brunch = self.root.LeftChild
            oppesite_Brunch = self.root.RightChild
        else:
            next_Brunch = self.root.RightChild
            oppesite_Brunch = self.root.LeftChild

        p_NB = next_Brunch.search_k_nearst_in_tree(Point,k)
        k_Best = insert_into_k_closest_point(Point,p_NB,self.root.pivot,k)

        worst_distance = distance_sq(Point,k_Best[-1][1])

        if  worst_distance > distance_sq_Ball(Point, oppesite_Brunch.root.pivot[1], \
                                                    oppesite_Brunch.root.radius_sq )   or len(k_Best) < k:
            p_OB = oppesite_Brunch.search_k_nearst_in_tree(Point,k)
            for p in p_OB:
                k_Best = insert_into_k_closest_point(Point,k_Best,p,k)
            #worst_distance = distance_sq(Point,k_Best[-1][1])
        return k_Best

def f_D_k_generator(DataSet,k):
    leafsize = 20
    data_tree = Ball_Tree(DataSet,[-1,1],leafsize)
    def f_D_k(Point):
        k_nearst = data_tree.search_k_nearst_in_tree(Point,k)
        summ = 0
        for x in k_nearst:
            summ += x[0]
        if summ >= 0:
            return 1
        else:
            return -1
    return f_D_k
     
def ErrorCal(func,TestSet):
    m = len(TestSet)
    Error = 0
    for labeled_point in TestSet:
        if labeled_point[0] != func(labeled_point[1]):
            Error += 1
    Error = Error/m
    return Error

# Define f_D_k function
def classify (name,KSET,l):
    # read the data
    trainSet = read_csv(name,"train")
    # randomly divide the data
    shuffle(trainSet)
    m = int(len(trainSet)/l)
    divided_trainSet = []
    for i in range(0,len(trainSet),m):
        divided_trainSet.append(trainSet[i:i+m])
    k_star = None
    min_Error = 1
    for k in KSET:
        sum_Error = 0
        f_D_k_list = []
        for i in range(l): 
            local_trainSet = [x for j in range(l) for x in divided_trainSet[j] if j != i]
            local_testSet = divided_trainSet[i]
            f_D_k = f_D_k_generator(local_trainSet,k)
            f_D_k_list.append(f_D_k)
            sum_Error += ErrorCal(f_D_k,local_testSet)
        average_Error = sum_Error/l
        if average_Error < min_Error:
            k_star = k
            def f_D_k_result(Point):
                summ = 0
                for func in f_D_k_list:
                    summ +=  func(Point)
                if summ >= 0:
                    return 1
                else:
                    return -1
    
    return [k_star,f_D_k_result]

# Test with file
name = 'bananas-1-2d'
start_time = time.time()
KSET = [1,2,3,4,5,6,7,8,9,10]
l = 5
k, f = classify (name,KSET,l)
testSet = read_csv(name,'test')
E = ErrorCal(f,testSet)
print(E)
run_time = time.time()-start_time
print(run_time)

# Test with small data

    
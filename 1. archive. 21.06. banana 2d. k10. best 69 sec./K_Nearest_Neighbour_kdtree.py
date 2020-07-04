import csv
import math
import time
from enum import Enum
from random import shuffle


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

# Define some useful functions
def distance_sq(p1,p2):
    n = len(p1)
    d = 0
    for i in range(n):
        d += (p1[i]-p2[i])**2
    return d

# special for the case, we have label in each point in the PSet
def k_closest_point(p,pSet,k):
    for q in pSet:
        q.append(distance_sq(p,q[1]))
    pSet = sorted(pSet,key = lambda point: point[2])
    for q in pSet:
        q.remove(q[-1])
        #print(q)
    return pSet[:k]

# special for the case, we have label in each point in the orderdSet and newpoint
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


def farthest_point(p,PSet):
    farthest = p
    for q in PSet:
        if distance_sq(p,q[1]) > distance_sq(p,farthest[1]):
            farthest = q
    return farthest


class Kd_Node:
    def __init__(self, Data):
        self.Data = Data
        self.LeftChild = None
        self.RightChild = None
        self.position = None
        self.pivot = None

class Position(Enum):
    InsidePoint = 1
    Leaf = 2

# Define the kd-tree class.
class Kd_Tree:    
    def __init__(self, trainData, trainLabel, leafsize=1, depth=0):
        self.label = trainLabel
        self.depth = depth
        self.root = None
        self.leafsize = leafsize
        if len(trainData) > 0:
            self.d = len(trainData[0][1])
            self.creat_tree(trainData)
        
    def creat_tree(self,DataSet):
        n = len(DataSet)
        self.root = Kd_Node(DataSet)
        if n <= self.leafsize:
            self.root.position = Position.Leaf
        else:
            self.root.position = Position.InsidePoint
            axis = self.depth % self.d
            sorted_points = sorted(DataSet, key = lambda point: point[1][axis])
            self.root.pivot = sorted_points[int(n/2)]
            #print(self.depth,self.root.pivot,sorted_points[:int(n/2)],sorted_points[int(n/2)+1:])
            self.root.LeftChild = Kd_Tree(sorted_points[:int(n/2)], self.label, self.depth + 1,self.leafsize)
            self.root.RightChild = Kd_Tree(sorted_points[int(n/2)+1:], self.label, self.depth + 1,self.leafsize)
    
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
        
        axis = self.depth % self.d
        next_Brunch = None
        oppesite_Brunch = None

        if Point[axis] < self.root.pivot[1][axis]:
            next_Brunch = self.root.LeftChild
            oppesite_Brunch = self.root.RightChild
        else:
            next_Brunch = self.root.RightChild
            oppesite_Brunch = self.root.LeftChild

        p_NB = next_Brunch.search_k_nearst_in_tree(Point,k)
        k_Best = insert_into_k_closest_point(Point,p_NB,self.root.pivot,k)

        worst_distance = distance_sq(Point,k_Best[-1][1])
        #print(len(k_Best))
        if  worst_distance > (Point[axis] - self.root.pivot[1][axis])**2 or len(k_Best) < k:
            p_OB = oppesite_Brunch.search_k_nearst_in_tree(Point,k)
            for p in p_OB:
                k_Best = insert_into_k_closest_point(Point,k_Best,p,k)
            #worst_distance = distance_sq(Point,k_Best[-1][1])
        return k_Best

def f_D_k_generator(DataSet,k):
    leafsize = 20
    data_tree = Kd_Tree(DataSet,[-1,1],leafsize)
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

#Test
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

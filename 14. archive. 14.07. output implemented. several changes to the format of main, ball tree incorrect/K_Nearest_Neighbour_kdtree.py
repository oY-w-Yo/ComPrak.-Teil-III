from random import shuffle
from read_and_write import read_csv
import numpy as np
import Assistant_class as AC
import Assistant_function as AF
import time
import copy

class Kd_Node:
    def __init__(self, Data):
        #self.position = position
        self.axis = 0

        self.Data = Data
        self.pivot = None

        self.LeftChild = None
        self.RightChild = None
        
        self.create_kd_node()
    
    def create_kd_node(self):
        n = len(self.Data)
        if n <= Leafsize:
            self.position = AC.Position.Leaf
        else:
            self.position = AC.Position.InsidePoint
            sorted_points,self.axis = AF.axis_find(self.Data,dimension)
            self.pivot = sorted_points[int(n/2)]
            self.LeftChild  = Kd_Node(sorted_points[:int(n/2)])
            self.RightChild = Kd_Node(sorted_points[int(n/2):])

    def stacking_from_kd_node(self,Point):
        #stacking_start = time.time()
        current_node = self
        Stack = [current_node]
        while current_node.position != AC.Position.Leaf:
            axis = current_node.axis
            if Point[axis] < current_node.pivot[1][axis]:
                current_node = current_node.LeftChild
            else:
                current_node = current_node.RightChild
            Stack.append(current_node)
        #print('stacking for len {} costs {}'.format(len(Stack),time.time()-stacking_start))
        return Stack

    def search_k_nearst_from_kd_node(self,Point,k):
        #Stack = [self]
        #search_start = time.time()
        Stack = self.stacking_from_kd_node(Point)
        k_Best = []
        distance_set = []
        #count = 0
        while Stack != []:
            #count += 1
            #print('iteration={}, current-len of stack {}'.format(count,len(Stack)))
            current_node = Stack.pop()
            if current_node.position == AC.Position.Leaf:
                local_k_best,local_distance_set = AF.k_closest_point(Point,current_node.Data,k)
                k_Best,distance_set = AF.merge_two_k_best(k_Best,distance_set,local_k_best,local_distance_set,k)
            else:
                axis = current_node.axis
                if len(k_Best) < k or distance_set[-1] > abs(Point[axis] - current_node.pivot[1][axis]):
                    if Point[axis] < current_node.pivot[1][axis]:
                        current_node = current_node.RightChild
                    else:
                        current_node = current_node.LeftChild
                    #Stack.append(current_node)
                    Stack.extend(current_node.stacking_from_kd_node(Point))
        #print('search in Data_size {} costs {}'.format(len(self.Data),time.time()-search_start))
        return k_Best,distance_set

# Define f_D_k function
def classify_kd (name,KSET,l,Folder,shufflee=True):

    k_star = None
    k_max = max(KSET)

    global Leafsize 
    Leafsize = int(k_max*0.9) + 1 

    # read the data
    trainSet = read_csv(name,Folder,"train")

    # set dimension
    global dimension
    dimension = len(trainSet[0][1])

    # randomly divide the data
    if shufflee == True:
        shuffle(trainSet)
    m = int(len(trainSet)/l)
    divided_trainSet = []
    for i in range(0,len(trainSet),m):
        divided_trainSet.append(trainSet[i:i+m])

    # build the tree 
    tree_root_list_with_i = []
    k_max_best = [] # in form [[Point_in_i,k_max_best_in_without_i,sum_label],...,]
    for i in range(l):
        local_trainSet = [x for j in range(l) for x in divided_trainSet[j] if j != i]
        start2 = time.time()
        root_node_without_i     = Kd_Node(local_trainSet) 
        root_node_with_i        = Kd_Node(divided_trainSet[i]) 
        print("l={},tree_build".format(i),time.time()-start2)
        tree_root_list_with_i.append(root_node_with_i)
        # search the max_k nearst Element of each local_train_set and store them in the list
        start2 = time.time()
        for p in divided_trainSet[i]:
            k_max_best_in_without_i,_ = root_node_without_i.search_k_nearst_from_kd_node(p[1],k_max)
            # add a new list to store the accumulated sum of label 
            sum_label = []
            sum_label.append(k_max_best_in_without_i[0][0])
            for j in range(1,len(k_max_best_in_without_i)):
                sum_label.append(sum_label[j-1] + k_max_best_in_without_i[j][0])
            k_max_best.append([p,k_max_best_in_without_i,sum_label])
        print("l={},tree_search".format(i),time.time()-start2)
    
    # for every k in KSET, evaluate the error and find the best k_star
    min_Error = 1
    for k in KSET:
        average_Error = np.mean([AF.point_error(p[0],p[2][k-1]) for p in k_max_best])
        #print(average_Error)
        if average_Error < min_Error:
            min_Error = average_Error
            k_star = k

    def f_D_k_result(Point):
        k_star_best = [] # in form [[Label,Vector,distance_from_Point,i],...,] <- len = k_star
        for i in range(l):
            k_star_best_in_i,distance_set_in_i = tree_root_list_with_i[i].search_k_nearst_from_kd_node(Point,k_star)
            for m in range(k_star):
                k_star_best_in_i[m].append(distance_set_in_i[m]) 
                k_star_best_in_i[m].append(i) 
            k_star_best.extend(k_star_best_in_i)
        
        k_star_best = sorted(k_star_best, key = lambda p: p[2])
        #print(Point,k_star_best)

        temp_summ = 0
        summ = 0
        for i in range(l):
            count = 0
            for p in k_star_best:
                if p[3] != i:
                    temp_summ += p[0]
                    count += 1 
                if count >= k:
                    break
            if temp_summ < 0:
                summ -= 1
            else:
                summ += 1
        if summ < 0:
            return -1,k_star_best
        else:
                return 1,k_star_best

    return k_star,f_D_k_result
    
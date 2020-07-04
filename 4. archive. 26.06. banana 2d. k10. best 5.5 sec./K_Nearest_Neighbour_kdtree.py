from random import shuffle
from read_and_write import read_csv
import Assistant_class as AC
import Assistant_function as AF
import time
import copy

class Kd_Node:
    def __init__(self, Data, parent = None, position = None, depth = 0):
        self.position = position
        self.depth = depth

        self.Data = Data
        self.pivot = None

        self.LeftChild = None
        self.RightChild = None
        self.parent = parent
        self.oppesite = None
        
        self.create_kd_node()
    
    def create_kd_node(self):
        n = len(self.Data)
        if n <= Leafsize:
            self.position = AC.Position.Leaf
        else:
            axis = self.depth % dimension
            sorted_points = sorted(self.Data, key = lambda point: point[1][axis])
            self.pivot = sorted_points[int(n/2)]
            self.LeftChild  = Kd_Node(sorted_points[:int(n/2)], parent=self, depth = self.depth+1)
            self.RightChild = Kd_Node(sorted_points[int(n/2):], parent=self, depth = self.depth+1)
            self.LeftChild.oppesite = self.RightChild
            self.RightChild.oppesite = self.LeftChild

    def descending_from_kd_node(self,Point):
        current_node = self
        while current_node.position != AC.Position.Leaf:
            axis = current_node.depth % dimension
            if Point[axis] < current_node.pivot[1][axis]:
                current_node = current_node.LeftChild
            else:
                current_node = current_node.RightChild
        return current_node
    
    def search_k_nearst_from_kd_node(self,Point,k):
        node_depth = self.depth
        current_node = self.descending_from_kd_node(Point)
        k_Best = AF.k_closest_point(Point,current_node.Data,k)
        radius_sq = AF.distance_sq(Point,k_Best[-1][1])

        while current_node.depth != node_depth:
            axis = current_node.parent.depth % dimension
            if radius_sq > (Point[axis] - current_node.parent.pivot[1][axis])**2:
                new_Best = current_node.oppesite.search_k_nearst_from_kd_node(Point,k)
                temp_Best = k_Best + new_Best
                temp_Best = sorted(temp_Best, key = lambda p: AF.distance_sq(p[1],Point))
                k_Best = temp_Best[:k]
                radius_sq = AF.distance_sq(Point,k_Best[-1][1])
            current_node = current_node.parent
        return k_Best

def f_D_k_generator_kd(kd_node,k):
    def f_D_k(Point):
        k_nearst= kd_node.search_k_nearst_from_kd_node(Point,k)
        summ = sum([x[0] for x in k_nearst])
        if summ >= 0:
            return 1
        else:
            return -1
    return f_D_k

# Define f_D_k function
def classify_kd (name,KSET,l):

    global Leafsize 
    Leafsize = max(KSET)*2

    # read the data
    trainSet = read_csv(name,"train")

    # set dimension
    global dimension
    dimension = len(trainSet[0][1])

    # randomly divide the data
    shuffle(trainSet)
    m = int(len(trainSet)/l)
    divided_trainSet = []
    for i in range(0,len(trainSet),m):
        divided_trainSet.append(trainSet[i:i+m])

    k_star = None
    k_max = max(KSET)


    # build the tree 
    tree_root_list_without_i = []
    tree_root_list_with_i = []
    k_max_best = [] # in form [[Point_in_i,k_max_best_in_without_i],...,]
    for i in range(l):
        local_trainSet = [x for j in range(l) for x in divided_trainSet[j] if j != i]
        start2 = time.time()
        root_node_without_i     = Kd_Node(local_trainSet,position=AC.Position.root)
        root_node_with_i        = Kd_Node(divided_trainSet[i],position=AC.Position.root)
        print("l={},tree_build".format(i),time.time()-start2)
        tree_root_list_without_i.append(root_node_without_i)
        tree_root_list_with_i .append(root_node_with_i)
        # search the max_k nearst Element of each local_train_set and store them in the list
        start2 = time.time()
        for p in divided_trainSet[i]:
            k_best = root_node_without_i.search_k_nearst_from_kd_node(p[1],k_max)
            k_max_best.append([p,k_best])
        print("l={},tree_search".format(i),time.time()-start2)
    
    # for every k in KSET, evaluate the error and find the best k_star
    min_Error = 1
    for k in KSET:
        m = len(k_max_best)
        sum_Error = sum([AF.evaluate(p[0],p[1][:k]) for p in k_max_best])
        average_Error = sum_Error/m
        #print(average_Error)
        if average_Error < min_Error:
            min_Error = average_Error
            k_star = k
    
    # 
   
    def f_D_k_result(Point):
        k_star_best = []
        k_star_result = []
        for i in range(l):
            k_star_best_in_i = tree_root_list_with_i[i].search_k_nearst_from_kd_node(Point,k_star)
            for p in k_star_best_in_i:
                p.append(AF.distance_sq(p[1],Point))
            k_star_best.append(k_star_best_in_i)
        #k_star_best = [p for p_list in k_star_best_in_i for p in p_list ]
        #k_star_best.sort(key=lambda p: AF.distance_sq(p[1],Point))
        #k_star_result = []
        for i in range(l):
            k_temp = [p for j in range(l) for p in k_star_best[j] if j != i]
            k_temp = sorted(k_temp, key = lambda p: p[2] )
            k_star_result.extend(k_temp[:k_star])
        summ = sum([x[0] for x in k_star_result])
        #summ = sum([f_D_k_generator_kd(tree_root_list_without_i[i],k_star)(Point) for i in range(l)])
        if summ >= 0:
            return 1
        else:
            return -1
    return [k_star,f_D_k_result]



from random import shuffle
from read_and_write import read_csv
import Assistant_class as AC
import Assistant_function as AF
import time

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
            sorted_points = sorted(self.Data, key = lambda point: point.get('Vector')[axis])
            self.pivot = sorted_points[int(n/2)]
            self.LeftChild  = Kd_Node(sorted_points[:int(n/2)], parent=self, depth = self.depth+1)
            self.RightChild = Kd_Node(sorted_points[int(n/2):], parent=self, depth = self.depth+1)
            self.LeftChild.oppesite = self.RightChild
            self.RightChild.oppesite = self.LeftChild

    def descending_from_kd_node(self,Point):
        current_node = self
        while current_node.position != AC.Position.Leaf:
            axis = current_node.depth % dimension
            if Point[axis] < current_node.pivot.get('Vactor')[axis]:
                current_node = current_node.LeftChild
            else:
                current_node = current_node.RightChild
        return current_node
    
    def search_k_nearst_from_kd_node(self,Point,k):
        node_depth = self.depth
        current_node = self.descending_from_kd_node(Point)
        k_Best = AF.k_closest_point(Point,current_node.Data,k)
        radius_sq = k_Best[-1].get('DistanceToPoint')

        while current_node.depth != node_depth:
            axis = current_node.parent.depth % dimension
            if radius_sq > (Point[axis] - current_node.parent.pivot[1][axis])**2:
                new_Best = current_node.oppesite.search_k_nearst_from_kd_node(Point,k)
                temp_Best = k_Best + new_Best
                temp_Best = sorted(temp_Best, key = lambda p: p.get('DistanceToPoint'))
                k_Best = temp_Best[:k]
                radius_sq = k_Best[-1].get('DistanceToPoint')
            current_node = current_node.parent
        return k_Best

def f_D_k_generator_kd(kd_node,k):
    def f_D_k(Point):
        k_nearst= kd_node.search_k_nearst_from_kd_node(Point,k)
        return sum([x[0] for x in k_nearst])
    return f_D_k

def k_best_generator_kd(kd_node,k):
    def k_best(Point):
        return kd_node.search_k_nearst_from_kd_node(Point,k)
    return k_best_generator_kd

def k_best_joiner_without_i(k_best_list,i):
    def k_best_witiout_i(Point):
        k_best = sum([k_best_list[j](Point) for j in range(len(k_best_list))  if j != i])
        k_best = sorted


# Define f_D_k function
def classify_kd (name,KSET,l):

    global Leafsize 
    Leafsize = max(KSET)*2

    # read the data
    trainSet = read_csv(name,"train")

    # set dimension
    global dimension
    dimension = len(trainSet[0].get('Vektor'))

    # randomly divide the data
    shuffle(trainSet)
    m = int(len(trainSet)/l)
    divided_trainSet = []
    for i in range(0,len(trainSet),m):
        divided_trainSet.append(trainSet[i:i+m])

    k_star = None
    min_Error = 1


    # build the tree
    tree_root_list_without_i = []
    tree_root_list_with_i = []
    for i in range(l):
        local_trainSet = [x for j in range(l) for x in divided_trainSet[j] if j != i]
        start2 = time.time()
        root_node_without_i     = Kd_Node(local_trainSet,position=AC.Position.root)
        root_node_with_i        = Kd_Node(divided_trainSet[i],position=AC.Position.root)
        print("l={},tree_build".format(i),time.time()-start2)
        tree_root_list_without_i.append(root_node_without_i)
        tree_root_list_with_i .append(root_node_with_i)

    # for every k in KSET, find f_d_k_result and the error of f_d_k
    for k in KSET:
        sum_Error = 0
        Target_point = []
        print("fdk start for k={}".format(k))
        start3 = time.time()
        
        k_best_in_i = [k_best_generator_kd(tree_root_list_with_i,k) for i in range(i)]
        #k_best_value_sum_in_i =[f_D_k_generator_kd(tree_root_list_with_i) for i in range(l)]
        k_best_witiout_i = 


            local_testSet = divided_trainSet[i]

            print("k={},l={}".format(k,i))
            strat4 = time.time()
            f_D_k = f_D_k_generator_kd(tree_root_list_without_i[i],k)
            print("end one fdk bild",time.time()-strat4)
            f_D_k_list.append(f_D_k)
            print("error-cal for k={},l={}".format(k,i))
            strat5 = time.time()
            sum_Error += AF.ErrorCal(f_D_k,local_testSet)
            print("end error-cal",time.time()-strat5)
        print("fdk end for k={}".format(k),time.time()-start3)
        average_Error = sum_Error/l
        print("assign start for k={}".format(k))
        start6 = time.time()
        if average_Error < min_Error:
            min_Error = average_Error
            k_star = k
            def f_D_k_result(Point):
                summ = sum([func(Point) for func in f_D_k_list])
                if summ >= 0:
                    return 1
                else:
                    return -1
        print("assign end for k={}".format(k),time.time()-start6)

    return [k_star,f_D_k_result]

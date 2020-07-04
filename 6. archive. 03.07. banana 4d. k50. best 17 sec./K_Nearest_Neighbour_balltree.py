from random import shuffle
from read_and_write import read_csv
import Assistant_class as AC
import Assistant_function as AF
class Ball_Node:
    def __init__(self, Data):
        self.Data = Data
        self.LeftChild = None
        self.RightChild = None
        self.position = None
        self.pivot = None # here is the pivot point also the center point
        self.radius_sq = None
        self.greatest_direction = AF.greatest_spread(Data)
        self.sorted_data = None
        self.creat_Ball_Node()
    
    def creat_Ball_Node(self):
        Dataset =self.Data
        w = self.greatest_direction
        self.sorted_data = sorted(Dataset,key = lambda point: AF.projection(w,point[1]))
        n = len(self.sorted_data)
        self.pivot = self.sorted_data[int(n/2)]
        p = self.pivot
        self.radius_sq = AF.distance_sq(AF.farthest_point(p[1],Dataset)[1], p[1])


# Define the Ball-tree class.
class Ball_Tree:    
    def __init__(self, trainData, trainLabel, leafsize=10, depth=0):
        self.label = trainLabel
        self.depth = depth
        self.root = None
        self.leafsize = leafsize

        if len(trainData) > 0:
            self.d = len(trainData[0][1])
            self.creat_Ball_tree(trainData)

    def creat_Ball_tree(self,DataSet):
        n = len(DataSet)
        self.root = Ball_Node(DataSet)
        if n <= self.leafsize:
            self.root.position = AC.Position.Leaf
        else:
            self.root.position = AC.Position.InsidePoint
            self.root.LeftChild = Ball_Tree(self.root.sorted_data[:int(n/2)], self.label, self.depth + 1,self.leafsize)
            self.root.RightChild = Ball_Tree(self.root.sorted_data[int(n/2)+1:], self.label, self.depth + 1,self.leafsize)
    
    def print_tree(self):
        if self.root is not None:
            if self.root.position == AC.Position.Leaf:
                print(len(self.root.Data),self.root.Data)
            else:
                print(self.root.pivot)
                if (self.root.LeftChild is not None) and (self.root.RightChild is not None):
                    self.root.LeftChild.print_tree()
                    self.root.RightChild.print_tree()

    def search_k_nearst_in_Ball_tree(self, Point, k=1):
        if self.root.position == AC.Position.Leaf:
            if len(self.root.Data) == 0 or self.root == None:
                return None
            else:
                k_Best = AF.k_closest_point(Point,self.root.Data,k)
                return k_Best
        
        next_Brunch = None
        oppesite_Brunch = None
        w = self.root.greatest_direction
        if  AF.projection(w,Point)< AF.projection(w,self.root.pivot[1]):
            next_Brunch = self.root.LeftChild
            oppesite_Brunch = self.root.RightChild
        else:
            next_Brunch = self.root.RightChild
            oppesite_Brunch = self.root.LeftChild

        p_NB = next_Brunch.search_k_nearst_in_Ball_tree(Point,k)
        k_Best = AF.insert_into_k_closest_point(Point,p_NB,self.root.pivot)

        worst_distance = AF.distance_sq(Point,k_Best[-1][1])

        if  worst_distance > AF.distance_sq_Ball(Point, oppesite_Brunch.root.pivot[1], \
                                                    oppesite_Brunch.root.radius_sq )   or len(k_Best) < k:
            p_OB = oppesite_Brunch.search_k_nearst_in_Ball_tree(Point,k)
            for p in p_OB:
                k_Best = AF.insert_into_k_closest_point(Point,k_Best,p)
            #worst_distance = distance_sq(Point,k_Best[-1][1])
        return k_Best

def f_D_k_generator_Ball(DataSet,k):
    leafsize = 20
    data_tree = Ball_Tree(DataSet,[-1,1],leafsize)
    def f_D_k(Point):
        k_nearst = data_tree.search_k_nearst_in_Ball_tree(Point,k)
        summ = 0
        for x in k_nearst:
            summ += x[0]
        if summ >= 0:
            return 1
        else:
            return -1
    return f_D_k
     
# Define f_D_k function
def classify_Ball (name,KSET,l):
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
            f_D_k = f_D_k_generator_Ball(local_trainSet,k)
            f_D_k_list.append(f_D_k)
            sum_Error += AF.ErrorCal(f_D_k,local_testSet)
        average_Error = sum_Error/l
        if average_Error < min_Error:
            min_Error = average_Error
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



    
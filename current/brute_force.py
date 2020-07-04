from read_and_write import read_csv
from Assistant_function import ErrorCal, distance_sq,k_closest_point
import time
from random import shuffle

def f_D_k_generator(DataSet,k):
    def f_D_k(Point):
        k_nearst = k_closest_point(Point,DataSet,k)
        summ = 0
        for x in k_nearst:
            summ += x[0]
        if summ >= 0:
            return 1
        else:
            return -1
    return f_D_k

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

    # for every k in KSET, find f_d_k_result and the error of f_d_k
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

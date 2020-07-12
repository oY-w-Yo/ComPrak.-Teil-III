from read_and_write import read_csv
from Assistant_function import ErrorCal, distance_sq,k_closest_point,point_error
import time
import numpy as np
from random import shuffle
from K_Nearest_Neighbour_balltree import classify_Ball
from K_Nearest_Neighbour_kdtree import classify_kd

# Define f_D_k function
def classify1 (name,KSET,l):
    k_star = None
    k_max = max(KSET)

    # read the data
    trainSet = read_csv(name,"train")

    # randomly divide the data
    #shuffle(trainSet)
    m = int(len(trainSet)/l)
    divided_trainSet = []
    for i in range(0,len(trainSet),m):
        divided_trainSet.append(trainSet[i:i+m])

    # build the tree 
    k_max_best = [] # in form [[Point_in_i,k_max_best_in_without_i,sum_label],...,]
    for i in range(l):
        local_trainSet = [x for j in range(l) for x in divided_trainSet[j] if j != i]
        # search the max_k nearst Element of each local_train_set and store them in the list
        for p in divided_trainSet[i]:
            k_max_best_in_without_i,_= k_closest_point(p[1],local_trainSet,k_max)
            # add a new list to store the accumulated sum of label 
            sum_label = []
            sum_label.append(k_max_best_in_without_i[0][0])
            for j in range(1,len(k_max_best_in_without_i)):
                sum_label.append(sum_label[j-1] + k_max_best_in_without_i[j][0])
            k_max_best.append([p,k_max_best_in_without_i,sum_label])
    
    # for every k in KSET, evaluate the error and find the best k_star
    min_Error = 1
    for k in KSET:
        #average_Error = np.mean([AF.Error(p[0],p[1][:k]) for p in k_max_best])
        average_Error = np.mean([point_error(p[0],p[2][k-1]) for p in k_max_best])
        #print(average_Error)
        if average_Error < min_Error:
            min_Error = average_Error
            k_star = k

    def f_D_k_result(Point):
        k_star_best = [] # in form[[Label,Vector,distance_from_Point,i],...,] <- len = k_star
        #k_star_result = []
        for i in range(l):
            k_star_best_in_i,distance_set_in_i= k_closest_point(Point,divided_trainSet[i],k_star)
            for m in range(k_star):
                k_star_best_in_i[m].append(distance_set_in_i[m]) 
                k_star_best_in_i[m].append(i) 
            k_star_best.extend(k_star_best_in_i)
        
        k_star_best = sorted(k_star_best, key = lambda p: p[2])
        print(Point,k_star_best)

        summ = 0
        for i in range(l):
            count = 0
            for p in k_star_best:
                if p[3] != i:
                    summ += p[0]
                    count += 1 
                if count >= k:
                    break

            #k_temp = [p for p in k_star_best if p[3] != i]
            #k_star_result.extend(k_temp[:k_star])
            #summ += sum(x[0] for x in k_temp[:k_star])

        if summ >= 0:
            return 1
        else:
            return -1

    return [k_star,f_D_k_result]


#Test
name = 'smallset'
start_time = time.time()
KSET = [1,2,3,4,5,6,7,8,9,10]
l = 5
k1, f1 = classify1 (name,KSET,l)
k2, f2 = classify_kd(name,KSET,l)

testSet = read_csv(name,'test')

for t in testSet:
    print('brtf')
    print(f1(t[1]))
    print('kd')
    print(f2(t[1]))
    print('\n')

run_time = time.time()-start_time
print(run_time)

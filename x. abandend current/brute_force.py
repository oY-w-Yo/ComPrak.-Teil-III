from read_and_write import read_csv
import Assistant_function as AF
import time
import copy
import numpy as np
from random import shuffle
from K_Nearest_Neighbour_kdtree import classify_kd
from K_Nearest_Neighbour_balltree import classify_ball

# Define f_D_k function
def brute_force(name,KSET,l,Folder):
    start_time1 = time.time()
    k_star = None
    k_max = max(KSET)

    global Leafsize 
    Leafsize = int(k_max * 0.9)+1

    # read the data
    trainSet = read_csv(name,Folder,"train")
    #trainSet = [[1,[-0.5,0.1]],[1,[-0.45,0.05]],[1,[-0.4,-0.1]],[1,[0,0]],[1,[0.5,0]],[1,[0.8,0]]]

    # set dimension
    global dimension
    dimension = len(trainSet[0][1])
    
    
    # randomly divide the data
    m = int(len(trainSet)/l)
    divided_trainSet = []
    for i in range(0,len(trainSet),m):
        divided_trainSet.append(trainSet[i:i+m])
    #print('Preparation=',time.time()-start_time1)

    k_max_best = [] # in form [[Point_in_i,k_max_best_in_without_i,sum_label],...,]
    print('search for k_max_best...')
    for i in range(l):
        start_time2 = time.time()
        local_trainSet = [x for j in range(l) for x in divided_trainSet[j] if j != i]
        # search the max_k nearst Element of each local_train_set and store them in the list
        for p in divided_trainSet[i]:
            k_max_best_in_without_i,_ = AF.k_closest_point(p[1],local_trainSet,k_max)
            # add a new list to store the accumulated sum of label 
            sum_label = []
            sum_label.append(k_max_best_in_without_i[0][0])
            for j in range(1,len(k_max_best_in_without_i)):
                sum_label.append(sum_label[j-1] + k_max_best_in_without_i[j][0])
            k_max_best.append([p,k_max_best_in_without_i,sum_label])
        print('the {}-th slice costs{}sec.'.format(i,time.time()-start_time2))
    
    start_time3 = time.time()
    print('search for k_star')
    # for every k in KSET, evaluate the error and find the best k_star
    min_Error = 1
    for k in KSET:
        average_Error = np.mean([AF.point_error(p[0],p[2][k-1]) for p in k_max_best])
        #print(average_Error)
        if average_Error < min_Error:
            min_Error = average_Error
            k_star = k
    print('k_star ={}, search costs{}sec.'.format(k_star,time.time()-start_time3))

    def f_D_k_result(Point):
        k_star_best = [] # in form [[Label,Vector,distance_from_Point,i],...,] <- len = k_star
        for i in range(l):
            k_star_best_in_i,distance_set_in_i = copy.deepcopy(AF.k_closest_point(Point,divided_trainSet[i],k_star))
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
    

#Test
#name = 'smallset'
#name = 'bananas-2-2d'
#Folder = 'classification-artificial/'
#name,Folder = ['ijcnn1.5000','classification-real/']
name,Folder = ['australian','classification-real/']
#name,Folder =['toy-3d','classification-artificial/']
start_time = time.time()
KSET = range(1,2)
l = 2
_, f2 = classify_kd (name,KSET,l,Folder,shufflee=False)
print('k_closest_point runs {} times'.format(AF.k_closest_point.count))
AF.k_closest_point.count = 0
#_, f2 = classify_ball (name,KSET,l,Folder,shufflee=False)
_, f1 = brute_force (name,KSET,l,Folder)
print('k_closest_point runs {} times'.format(AF.k_closest_point.count))
testSet = read_csv(name,Folder,'test')
#testSet = [[1,[-0.45,0]]]
print("Test in ball start")
result1,E1 = AF.Test(f1,testSet)
print("Test in kd start")
result2,E2 = AF.Test(f2,testSet)
#print(result1,'\n')
#print(result2,'\n')
print('average_Error1=',E1)
print('average_Error2=',E2)
print('correct?',result1==result2)
#for i in range(len(result1)):
#    print(i,result1[i],'\n',result2[i],'\n')
run_time = time.time()-start_time
print(run_time)

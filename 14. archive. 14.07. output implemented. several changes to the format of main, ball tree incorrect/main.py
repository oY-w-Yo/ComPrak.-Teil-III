import time
import matplotlib.pyplot as plt
from read_and_write import read_csv, write_csv
from K_Nearest_Neighbour_balltree import classify_ball
from K_Nearest_Neighbour_kdtree import classify_kd
from Assistant_function import Test,k_closest_point



######################################################################################################
#                                         Main Function area                                         #
######################################################################################################
def main(data,KSET,l, Methode, repeat=1, plotting = False):
    sum_time = 0
    sum_Error = 0
    k_star = []
    for i in range(repeat):
        start_classify_time = time.time()
        l = 5
        # finding k* and generating f_D_k*
        if Methode == "kd":
            k, f = classify_kd(data[0],KSET,l,data[1])
        elif Methode == "ball":
            k, f = classify_ball(data[0],KSET,l,data[1])
        print('k_star = {}'.format(k))
        end_classify_time = time.time()
        # calculations for test set
        testSet = read_csv(data[0],data[1],'test')
        result , E = Test(f,testSet)
        print('Error = {}'.format(E))
        end_test_time = time.time()
        # result output 
        write_csv('classification result.csv',result)
        end_write_time = time.time()
        # time calculation
        run_time = end_write_time - start_classify_time
        build_time = end_classify_time - start_classify_time
        test_time = end_test_time - end_classify_time
        write_time = end_write_time - end_test_time
        print("classify_build = {:.5}, test = {:.5}, write = {:.5}, run={:.5}".format(build_time,test_time,write_time, run_time))
        sum_time += run_time
        sum_Error += E
        k_star.append(k)
    # generating average properties  
    if repeat > 1:
        sum_k_star = sum(k_star)
        plt.hist(k_star,align = 'left',rwidth=0.5)
        print(sorted(k_star))
        print("average_run_time = {:.5}, average_Error = {:.5}, average_k_star ={:.2}".\
                                        format(sum_time/repeat,sum_Error/repeat,sum_k_star/repeat))
        if plotting == True:
            plt.show()     

######################################################################################################
#                                         Configuration area                                         #
######################################################################################################

KSET = range(1,51)
l = 5

#data = ['bananas-1-2d','classification-artificial/']
data = ['bananas-1-4d','classification-artificial/']
#data = ['bananas-5-4d','classification-artificial/']
#data = ['toy-3d','classification-artificial/']
#data = ['toy-10d','classification-artificial/']
#data = ['smallset','classification-artificial/']

#data = ['australian','classification-real/']
#data = ['cod-rna.5000','classification-real/']
#data = ['ijcnn1','classification-real/']
#data = ['ijcnn1.10000','classification-real/']
#data = ['ijcnn1.5000','classification-real/']
#data = ['svmguide1','classification-real/']


######################################################################################################
#                                          Execution area                                            #
######################################################################################################
main(data,KSET,l,"kd",repeat=1)      # execute once
#main(data,KSET,l,"kd",repeat=3,plotting=False)    # execute several times to calculate average properties
#print('k_closest_point runs {} times'.format(k_closest_point.count))




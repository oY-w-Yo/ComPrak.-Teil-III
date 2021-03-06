import time
import matplotlib.pyplot as plt
from read_and_write import read_csv, write_csv
from K_Nearest_Neighbour_balltree import classify_ball
from K_Nearest_Neighbour_kdtree import classify_kd
from Assistant_function import Test,k_closest_point



######################################################################################################
#                                         Main Function area                                         #
######################################################################################################
def main(name,KSET,l,repeat, plotting = True):
    sum_time = 0
    sum_Error = 0
    k_star = []
    for i in range(repeat):
        start_time = time.time()
        l = 5
        #k, f = classify_kd(name,KSET,l,Folder)
        k, f = classify_ball(name,KSET,l,Folder)
        print('k_star = {}'.format(k))
        mittel_time = time.time()
        testSet = read_csv(name,Folder,'test')
        _,E = Test(f,testSet)
        print('Error = {}'.format(E))
        end_time = time.time()
        run_time = end_time-start_time
        build_time = mittel_time - start_time
        test_time = end_time - mittel_time
        sum_time += run_time
        sum_Error += E
        k_star.append(k)
        print("classify_build = {}, test = {}, run={}".format(build_time,test_time,run_time))
        ######## writing result into csv data, TBC #######
    if repeat > 1:
        sum_k_star = sum(k_star)
        plt.hist(k_star,align = 'left',rwidth=0.5)
        print(sorted(k_star))
        print("average_run_time = {}, average_Error = {}, average_k_star ={}".\
                                        format(sum_time/repeat,sum_Error/repeat,sum_k_star/repeat))
        if plotting == True:
            plt.show()     

######################################################################################################
#                                         Configuration area                                         #
######################################################################################################
#name = 'bananas-1-2d'
name = 'bananas-1-4d'
#name = 'bananas-5-4d'
#name = 'toy-3d'
#name = 'toy-10d'
#name = 'smallset'

#name = 'australian'
#name = 'cod-rna.5000'
#name = 'ijcnn1'
#name = 'ijcnn1.10000'
#name = 'ijcnn1.5000'
#name = 'svmguide1'


Folder = 'classification-artificial/'
#Folder = 'classification-real/'


KSET = range(1,51)
l = 5

######################################################################################################
#                                          Execution area                                            #
######################################################################################################
main(name,KSET,l,repeat=1)      # execute once
#main(name,KSET,l,repeat=10,plotting=False)    # execute several times to calculate average properties

print('k_closest_point runs {} times'.format(k_closest_point.count))




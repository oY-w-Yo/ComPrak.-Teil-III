import time
import matplotlib.pyplot as plt
from read_and_write import read_csv, write_csv
from K_Nearest_Neighbour_balltree import classify_ball
from K_Nearest_Neighbour_kdtree import classify_kd
from Assistant_function import ErrorCal


# Test with file
name = 'bananas-1-4d'
#name = 'bananas-1-2d'
#name = 'toy-10d'
#name = 'smallset'
sum_time = 0
sum_Error = 0
k_star = []
rounde = 5
for i in range(rounde):
    start_time = time.time()
    KSET = range(1,51)
    l = 5
    k, f = classify_kd(name,KSET,l)
    #k, f = classify_ball(name,KSET,l)
    print('k_star = ',k)
    mittel_time = time.time()
    testSet = read_csv(name,'test')
    E = ErrorCal(f,testSet)
    print('Error =',E)
    end_time = time.time()
    run_time = end_time-start_time
    sum_time += run_time
    sum_Error += E
    k_star.append(k)
    print("classity_build = {}, test = {}, run={}".format(mittel_time - start_time,end_time - mittel_time,run_time))
sum_k_star = sum(k_star)
plt.hist(k_star,align = 'left',rwidth=0.5)
print(sorted(k_star))
print("average_run_time = {}, average_Error = {}, average_k_star ={}".format(sum_time/rounde,sum_Error/rounde,sum_k_star/rounde))
plt.show()



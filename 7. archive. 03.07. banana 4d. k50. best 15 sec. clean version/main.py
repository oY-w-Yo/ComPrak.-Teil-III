import time
from read_and_write import read_csv, write_csv
from K_Nearest_Neighbour_balltree import classify_Ball
from K_Nearest_Neighbour_kdtree import classify_kd
from Assistant_function import ErrorCal


# Test with file
#name = 'bananas-1-4d'
name = 'bananas-1-2d'
#name = 'toy-10d'
#name = 'smallset'
KSET = range(1,11)
l = 5
def main_fun(name,KSET,l):
    start_time = time.time()
    k, f = classify_kd(name,KSET,l)
    print('k_star = ',k)
    mittel_time = time.time()
    testSet = read_csv(name,'test')
    E = ErrorCal(f,testSet)
    print('Error =',E)
    end_time = time.time()
    print("classity_build = {}, test = {}, run={}".format(mittel_time - start_time,end_time - mittel_time,end_time-start_time))

count = 0
for i in range(100):
    print('i=',i)
    try:
        main_fun(name,KSET,l)
    except :
        count += 1

print('count=',count)
    
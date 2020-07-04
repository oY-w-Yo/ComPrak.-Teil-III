import time
from read_and_write import read_csv
from read_and_write import write_csv
from K_Nearest_Neighbour_balltree import classify_Ball
from K_Nearest_Neighbour_kdtree import classify_kd
from Assistant_function import ErrorCal


# Test with file
name = 'bananas-1-2d'
start_time = time.time()
KSET = range(1,11)
l = 5
k, f = classify_kd(name,KSET,l)
mittel_time = time.time()
testSet = read_csv(name,'test')
E = ErrorCal(f,testSet)
print(E)
end_time = time.time()
print("classity_build = {}, test = {}, run={}".format(mittel_time - start_time,end_time - mittel_time,end_time-start_time))


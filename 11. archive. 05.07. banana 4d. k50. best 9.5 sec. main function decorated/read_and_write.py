import csv
import os
import numpy as np

# Read the Data from 

def read_csv(name,Settype):
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    File_csv = name + "." + Settype + ".csv"
    Path_csv = os.path.join(THIS_FOLDER, 'classification-artificial/',File_csv)
    with open(Path_csv) as File:
    #with open('classification-artificial/'+File_csv) as File:
        Data = csv.reader(File, delimiter=',')
        pointSet = []
        for point in Data:
            for i in range(len(point)):
                point[i] = float(point[i])
            #pointSet.append([ point[0], np.array(point[1:]) ])
            pointSet.append([ point[0], point[1:]])
    File.close()
    return pointSet


def write_csv(name,text):
    with open(name, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        t = []
        t.append(text)
        writer.writerow(t)
    output_file.close()


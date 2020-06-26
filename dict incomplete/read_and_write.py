import csv
import numpy as np

# Read the Data from 

def read_csv(name,Settype):
    File_csv = name + "." + Settype + ".csv"
    with open('classification-artificial/'+File_csv) as File:
        Data = csv.reader(File, delimiter=',')
        pointSet = []
        for point in Data:
            for i in range(len(point)):
                point[i] = float(point[i])
            pointSet.append({'Label':point[0], 'Vector':point[1:]})
    File.close()
    return pointSet


def write_csv(name,text):
    with open(name, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        t = []
        t.append(text)
        writer.writerow(t)
    output_file.close()


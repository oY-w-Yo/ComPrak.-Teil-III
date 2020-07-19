import csv
import os
import numpy as np

# Read the Data from 

def read_csv(name,Folder,Settype):
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    File_csv = name + "." + Settype + ".csv"
    Path_csv = os.path.join(THIS_FOLDER, Folder,File_csv)
    with open(Path_csv) as File:
        Data = csv.reader(File, delimiter=',')
        pointSet = []
        for point in Data:
            for i in range(len(point)):
                point[i] = float(point[i])
            #pointSet.append([ point[0], np.array(point[1:]) ])
            pointSet.append([ point[0], point[1:]])
    File.close()
    return pointSet


def write_csv(name,result):
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(THIS_FOLDER,'classification-results/', name)
    with open(csv_path, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        print(csv_path)
        for data in result:
            line = [data[2]]
            [ line.append(data[1][i]) for i in range(len(data[1])) ]
            writer.writerow(line)
    output_file.close()


import matplotlib.pyplot as plt
import numpy as np
from   random import choice

def plot2dData(DataSet,titel=""): 
    oneX = []
    oneY = []
    minusOneX = []
    minusOneY = []

    for p in DataSet:
        if p[0] == 1:
            oneX.append(p[1][0])
            oneY.append(p[1][1])
        else:
            minusOneX.append(p[1][0])
            minusOneY.append(p[1][1])
    plt.scatter(oneX, oneY, s=1,  c="r", alpha=0.6)
    plt.scatter(minusOneX, minusOneY, s=1, c="b", alpha=0.6)
    plt.title(titel)
    plt.savefig('./plot-results/'+titel+'.jpg')
    plt.show()

def plot2dData_with_point(DataSet,point,radius,titel=""): 
    oneX = []
    oneY = []
    minusOneX = []
    minusOneY = []

    for p in DataSet:
        if p[0] == 1:
            oneX.append(p[1][0])
            oneY.append(p[1][1])
        else:
            minusOneX.append(p[1][0])
            minusOneY.append(p[1][1])
    plt.scatter(oneX, oneY, s=1,  c="r", alpha=0.5)
    plt.scatter(minusOneX, minusOneY, s=1, c="b", alpha=0.5)
    #print(point)
    #print(point[0]==-1)
    if point[0] == 1:
        plt.scatter(point[1][0],point[1][1],s=10, c="r", alpha=1)
    if point[0] == -1:
        plt.scatter(point[1][0],point[1][1],s=10, c="b", alpha=1)

    left_down   = [point[1][0]-radius,point[1][1]-radius]
    left_up     = [point[1][0]-radius,point[1][1]+radius]
    right_down  = [point[1][0]+radius,point[1][1]-radius]
    right_up    = [point[1][0]+radius,point[1][1]+radius]

    plt.plot([left_down[0],left_up[0]],[left_down[1],left_up[1]],c = 'black')
    plt.plot([left_up[0],right_up[0]],[left_up[1],right_up[1]],c = 'black')
    plt.plot([right_up[0],right_down[0]],[right_up[1],right_down[1]],c = 'black')
    plt.plot([right_down[0],left_down[0]],[right_down[1],left_down[1]],c = 'black')

    plt.title(titel)
    plt.show()

def plott(trainset,testset,divided_trainset,result,k,file_name):
    # plot the whole classification_result
    classification_result = [[p[2],p[1]] for p in result]
    plot2dData(trainset, '{} trainset'.format(file_name[0]))
    plot2dData(testset, '{} testset'.format(file_name[0]))
    plot2dData(classification_result, '{} classification result for k* {}'.format(file_name[0],k))


    # choose a point randomly in result
    s = choice(result)

    # plot the result for s in slices
        # filter and get raduis and result in slices
    print("k={}".format(k))
    radius_list= []
    classification_for_p_list= []
    for i in range(len(divided_trainset)):
        count = 0
        temp_summ = 0
        for p in s[3]:
            if p[3] != i:
                count += 1 
                temp_summ += p[0]
            if count >= k:
                radius_list.append(p[2]) 
                break 
        if temp_summ < 0:
            classification_for_p_list.append(-1)
        else:
            classification_for_p_list.append(1)

    for i in range(len(divided_trainset)):
        local_trainSet = [x for j in range(len(divided_trainset)) for x in divided_trainset[j] if j != i]
        plot2dData_with_point(local_trainSet,[classification_for_p_list[i],s[1]],radius_list[i],'k* nearest in slices without {}'.format(i))

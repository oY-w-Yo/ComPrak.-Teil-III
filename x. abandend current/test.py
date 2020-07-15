
trainSet = [[1,[-0.5,0.1]],[1,[-0.45,0.05]],[1,[-0.4,-0.1]],[1,[0,0]],[1,[0.5,0]],[1,[0.8,0]]]
m = 3
divided_trainSet = []
for i in range(0,len(trainSet),m):
    divided_trainSet.append(trainSet[i:i+m])
print('divided_trainSet={}'.format(divided_trainSet))
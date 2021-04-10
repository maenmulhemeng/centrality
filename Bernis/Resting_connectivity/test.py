import networkx as nx
import scipy.io  as sio
import numpy as np
mat = sio.loadmat('resultsROI_Subject001_Condition001.mat')
print("-------------- start ---------------")
print(mat.keys())
#print(len(mat['Z'][0]))

#print(len(mat['names'][0]))
#for i in range(len(mat['names'][0])):
#    if (mat['names'][0][i] == mat['names2'][0][i]):
#        print(i,mat['names'][0][i][0])
#    else:
#        print("The different name in ",i)


#for v in mat['names2'][0]:
#    print(v[0])

# mat['SE'][0] is an array [1..167]
# print(mat['SE'][0])

# mat['DOF'] is a value
# print(mat['DOF'][0])

#for v in mat['regressors'][0][0]:
#    print(v)

#print(mat['xyz'])
#for v in mat['xyz'][0]:
#    print(v)


A = np.matrix(mat['Z'])
A = A[:,:164]
# print(A)
# A = np.pad(A, ((0,3), (0,0)), mode='constant', constant_values=0)
# print(A[0])
G = nx.from_numpy_matrix(A) 
print(nx.average_clustering(G))

#for v in mat['Z']:
#    print("---")
#    G = nx.from_numpy_matrix(v)
#    print("---")
#    print(len(mat['Z']))
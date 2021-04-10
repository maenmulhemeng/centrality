import networkx as nx
import scipy.io  as sio
import numpy as np

print("-------------- start ---------------")

for i in range(1,24):
    #print(i)

    mat = sio.loadmat('resultsROI_Subject'+ f'{i:03d}' +'_Condition001')
    print("-------------- Subject  ",i ," ---------------")
    #print(mat.keys())
    #print(mat['Z'][0])
    A = np.matrix(mat['Z'])
    A = A[:,:164]
    # A = np.pad(A, ((0,3), (0,0)), mode='constant', constant_values=0)
    #print(len(A))
    G = nx.from_numpy_matrix(A) 
    print("clustering coef",nx.average_clustering(G))
    print("degree cent",nx.degree_centrality(G))
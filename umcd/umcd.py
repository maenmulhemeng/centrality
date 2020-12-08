import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

B = np.loadtxt("icbm_thick_mat.txt")
G = nx.from_numpy_matrix(B)
mylabels = []
dic = {}

with open('fs_region_abbrev_sort.txt') as f:
    mylabels = f.read().splitlines()

for n in range(len(mylabels)):
    dic[n] = mylabels[n]
print(len(mylabels))
print(mylabels)

V = nx.edge_betweenness_centrality(G,68,False)

print(V)
print(V.get((24, 64)))



nx.draw(G,labels = dic,with_labels=True )
plt.show()
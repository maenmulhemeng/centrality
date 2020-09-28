import networkx as nx
import matplotlib.pyplot as plt


G = nx.Graph()
elist = [('a', 'b',1.0), ('a', 'f',1.0), ('b', 'f',1.0), ('b', 'e',1.0), ('b', 'c',1.0), ('c', 'e',1.0), ('c', 'd',1.0), ('e', 'f',1.0)]
G.add_weighted_edges_from(elist)
plt.subplot(122)
print(nx.betweenness_centrality(G,6,False))
nx.draw(G) 
plt.show()
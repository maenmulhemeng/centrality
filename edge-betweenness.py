import networkx as nx
import matplotlib.pyplot as plt


G = nx.Graph()
elist = [('a', 'b'), ('a', 'i'), ('b', 'c'), ('b', 'i'), ('c', 'd'), ('d', 'e'), ('e', 'f'), ('e', 'g'), ('e', 'h'), ('e', 'i'), ('g','h'), ('h','i')]
# elist = [('a', 'b'), ('a', 'd'), ('b','e'),('b','c'),('c','f'),('e','f'),('d','e')]
G.add_edges_from(elist)
plt.subplot(122)
print(nx.edge_betweenness_centrality(G,9,False))
nx.draw(G) 
plt.show()
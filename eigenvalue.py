import networkx as nx
import matplotlib.pyplot as plt


G = nx.path_graph(0)
# Fig 10.10: e has the heighest eigenvalue centrality
elist = [('a', 'b'), ('a', 'i'), ('b', 'c'), ('b', 'i'), ('c', 'd'), ('d', 'e'), ('e', 'f'), ('e', 'g'), ('e', 'h'), ('e', 'i'), ('g','h'), ('h','i')]

# another simple example
# elist = [('a', 'b'), ('b', 'd'), ('d', 'c'), ('d', 'e'), ('c', 'e')]


G.add_edges_from(elist)
plt.subplot(122)
centrality = nx.eigenvector_centrality(G)
print(['The node (%s) :  %0.2f'%(node,centrality[node]) for node in centrality])
nx.draw(G) 
plt.show()
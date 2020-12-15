import networkx as nx # graph
G = nx.Graph()
a = 0
b = 1 
c = 2
d = 3
p = 4
q = 5

L = [(a, d, 2), (a, p, 5), (a, q, 8),
     (b, d, 7), (b, p, 1), (b, q, 3),
     (c, d, 9), (c, p, 6), (c, q, 4)]
     
G.add_weighted_edges_from(L)
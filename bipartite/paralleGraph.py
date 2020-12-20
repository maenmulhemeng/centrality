import networkx as nx # graph
G = nx.Graph()
a = 0
b = 1 
c = 2
d = 3
p = 4
q = 5
r = 6
s = 7
L = [(a, p, 1), (a, q, 8), (a, r, 13), (a,s,2),
     (b, p, 15), (b, q, 14), (b, r, 6), (b,s,7),
     (c, p, 3), (c, q, 12), (c, r, 4), (c,s,16),
     (d, p, 11), (d, q, 10), (d, r, 5), (d,s,9)]
     
G.add_weighted_edges_from(L)
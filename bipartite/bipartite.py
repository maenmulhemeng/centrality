import networkx as nx # graph
import pylab as plt # plotting
#import testGraph as test
import hugeGraph as test
from collections import deque # queue

def select_heviest_edge(E):
    max = -1
    max_edge = ()
    
    for (u,v,w) in E:
        if (max < w):
            max = w
            max_edge = (u,v,w)
    return max_edge
def remove_incident(G,e):
    # print(G.edges)
    for (u,v) in G.edges:
        if ( u in e or v in e):
            G.remove_edge(u,v)
    return G.edges.data('weight', default=1)

def bipartite(G):
    Ew = G.edges.data('weight', default=1)
    M = []
    match_weight = 0
    
    while len(Ew) > 0:
        e = select_heviest_edge(Ew)
        M.append(e)
        match_weight = match_weight + e[2]
        Ew = remove_incident(G,e)
    return M


if __name__ == '__main__':
    
    nx.draw(test.G, with_labels=True)
    plt.savefig('graph.png')
    match = bipartite(test.G)
    print(match)
 
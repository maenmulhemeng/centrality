import networkx as nx # graph
import pylab as plt # plotting
from collections import deque # queue

def bipartite(A):
    compoenent_nodes = [s]
    Q = deque() # creates a new Queue object
    
    Q.append(s) # adds the source ‘s’ to the queue
    while len(Q) != 0: # is Q empty?
        u = Q.popleft() # dequeue from queue
        # add u to the current component
        # print('The node',u)
        # print('dd',d)
        # print(Q)
        for v in range(len(A[u])): # iterate thru the neighbors of ’u’
            # print('neighbours', A[u][v])
            if A[u][v] == 1 and v not in d: # ‘v’ is unvisited
                d[v] = d[u] + 1 # update shortest path distance of ‘v’
                parent[v] = u
                compoenent_nodes.append(v)
                Q.append(v) # add ‘v’ to the queue
    return compoenent_nodes

if __name__ == '__main__':

    # 0 1 2 3 4 5 6 7 8 
   # ------------------
# 0 | 0 1 0 0 1 0 0 0 0
# 1 | 1 0 1 1 1 0 0 0 0
# 2 | 0 1 0 1 0 0 0 0 0
# 3 | 0 1 1 0 1 1 0 0 0
# 4 | 1 1 0 1 0 0 0 0 0
# 5 | 0 0 0 1 0 0 1 0 0
# 6 | 0 0 0 0 0 1 0 0 0
# 7 | 0 0 0 0 0 0 0 0 1
# 8 | 0 0 0 0 0 0 0 1 0
 
    a = 0
    b = 1 
    c = 2
    d = 3
    p = 4
    q = 5

     
    V =  {a,b,c,d,p,q}
    n = len(V)
    A =[]
    for i in range(n):
        A.append([])
        for j in range(n):
            A[j].append(0)
    A[a][d] = 2
    A[a][p] = 5 
    A[a][q] = 8

    A[b][d] = 7
    A[b][p] = 1 
    A[b][q] = 3
    
    A[c][d] = 9 
    A[c][p] = 6 
    A[c][q] = 4

    match = bipartite(A)
    print(match)
   

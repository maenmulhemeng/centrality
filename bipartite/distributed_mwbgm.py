import networkx as nx # graph
import pylab as plt # plotting
import testGraph as example1
import hugeGraph as example2 
import paralleGraph as example3
from collections import deque # queue

import logging
import threading
import queue

def mergeTwoLists(test_list1, test_list2):
    size_1 = len(test_list1) 
    size_2 = len(test_list2)
    res = [] 
    i, j = 0, 0
    while i < size_1 and j < size_2: 
        if test_list1[i][2] > test_list2[j][2]: 
            res.append(test_list1[i]) 
            i += 1
        else: 
            res.append(test_list2[j]) 
            j += 1
    return res + test_list1[i:] + test_list2[j:] 

def include_in_matching(E):
    M = []
    selected = {}
    for (u,v,w) in E:
        if not selected.get(u) and not selected.get(v):
            M.append((u,v,w)) 
            selected[u] = (u,v,w)
            selected[v] = (u,v,w)
    return M

def sort_edges(E):
    e = len(E)
    for i in range(e):
        #print("process ", p, " : ", E[i][1])
        for j in range(i+1,e):
            
            if (E[i][2] < E[j][2]):
                temp = E[i]
                E[i] = E[j]
                E[j] = temp
    print("stop")
    return E


if __name__ == '__main__':
    k = 2 # number of process
    G = example3.G
    n = G.number_of_nodes()
    
    length = int(n/k)
    
    print("k = ",k)
    print("n = ",n)
    print("length =",length)
    # print("adjancy ",adj)
    process = []
    que = queue.Queue()
    adj = G.adjacency()
    for i in range(k):
        E1 = []
        count = 0
        
        for e in adj:
            #print(e)
            for j in e[1]:  
                #print(e[1][j]['weight'])
                E1.append((e[0],j,e[1][j]['weight']))
            count = count + 1
            if(count >= length):
                break
        #Thread(target=lambda q, arg1: q.put(foo(arg1)), args=(que, 'world!'))
        x = threading.Thread(target=lambda q, arg1: q.put(sort_edges(arg1)), args=(que, E1)) 
        #Thread(target=sort_edges, args=(E1,i,))
        process.append(x)
    
    print("start processing ", process)    
    
    for i in range(len(process)):
        print("start process ",i)
        process[i].start()

    
    all = []
    for i in range(len(process)):
        #print("join")
        process[i].join()
    # Check thread's return value
    result = []
    print("Now merge")
    while not que.empty():
        aList = que.get()
        #print(aList)
        #print(result)
        result = mergeTwoLists(result, aList)

    #print (result)

    match = include_in_matching(result)    

    print(match)
    print("all finished")

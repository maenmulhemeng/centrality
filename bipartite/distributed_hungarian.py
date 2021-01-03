import networkx as nx # graph
import pylab as plt # plotting
import testGraph as example1
import hugeGraph as example2 
import paralleGraph as example3
from collections import deque # queue

import logging
import threading
import queue
import sys


def get_min_from_row(G,row):
    print(G[row])
    min = sys.maxsize
    index = -1
    for i in range(len(G[row])):
        if (min > G[row][i]):
            min = G[row][i]
            index = i
    return min,index


def get_min_from_column(G,column):
    min = sys.maxsize
    index = -1
    for i in range(len(G)):
        if (min > G[i][column]):
            min = G[i][column]
            index = i
    return min,index


def subtract_min_from_rows(G):
    zeros_of_rows = []
    zeros_of_columns = []
    
    for i in range(len(G[0])):
        zeros_of_columns.append([])
    
    for row in range(len(G)):
        minimum = min(G[row])     
        zeros_of_rows.append([])
        for column in range(len(G[row])):
            
            x = G[row][column] - minimum
            # print(x)
            if x == 0 and G[row][column] != 0:
                #print("row[",row,"] =  ",column)

                zeros_of_rows[row].append(column)
                zeros_of_columns[column].append(row) 
           
            G[row][column] = x
    return G, zeros_of_rows,zeros_of_columns

def find_min_length(a):
    min = sys.maxsize
    min_index = -1
    for i in range(len(a)):
        if ( 0 < len(a[i]) < min):
            min = len(a[i])
            min_index = i
    return a[min_index], min_index


def subtract_min_from_columns(G):
    zeros_of_rows = []
    zeros_of_columns = []
    
    for i in range(len(G)):
        zeros_of_rows.append([])
    #print("len",len(G))
    for column in range(len(G[0])):
        zeros_of_columns.append([])

        res = [sub[column] for sub in G] 
        print(res)
        minimum = min(res)
        for row in range(len(res)):
            x = G[row][column] - minimum
            
            if x == 0 and G[row][column]!=0:
                #print("row[",row,"] =  ",column)
                zeros_of_rows[row].append(column)
                zeros_of_columns[column].append(row) 
            G[row][column] = x
    return G, zeros_of_rows,zeros_of_columns

def cover_zeros(zeros_of_rows, zeros_of_columns):
    zeros_of_rows_p = zeros_of_rows.copy()
    zeros_of_columns_p = zeros_of_columns.copy()

    number_of_lines = 0
    maximum_in_rows = max(zeros_of_rows_p, key = lambda x:len(x))
    index_of_max_in_rows = zeros_of_rows_p.index(maximum_in_rows)

    maximum_in_columns = max(zeros_of_columns_p, key = lambda x:len(x))
    index_of_maximum_in_columns = zeros_of_columns_p.index(maximum_in_columns)
    
    horizental_lines = []
    vertical_lines = []
    while (maximum_in_rows != [] and maximum_in_columns != []):
        #print(maximum_in_rows)
        #print(maximum_in_columns)
        #print(zeros_of_rows_p,zeros_of_columns_p)
        if (len(maximum_in_rows) >= len(maximum_in_columns)):
            horizental_lines.append(index_of_max_in_rows)
            for i in range(len(zeros_of_rows_p[index_of_max_in_rows])):
                index = zeros_of_rows_p[index_of_max_in_rows][i]
                zeros_of_columns_p[index].pop()
            zeros_of_rows_p[index_of_max_in_rows] = []
        else:
            vertical_lines.append(index_of_maximum_in_columns)
            for i in range(len(zeros_of_columns_p[index_of_maximum_in_columns])):
                index = zeros_of_columns_p[index_of_maximum_in_columns][i]
                
                zeros_of_rows_p[index].pop()
            zeros_of_columns_p[index_of_maximum_in_columns] = []
        maximum_in_rows = max(zeros_of_rows_p, key = lambda x:len(x))
        index_of_max_in_rows = zeros_of_rows_p.index(maximum_in_rows)

        maximum_in_columns = max(zeros_of_columns_p, key = lambda x:len(x))
        index_of_maximum_in_columns = zeros_of_columns_p.index(maximum_in_columns)

        
        number_of_lines = number_of_lines + 1   
    return number_of_lines , horizental_lines, vertical_lines
    
def assign_tasks_to_workers(zeros_of_rows, zeros_of_columns):
    zeros_of_rows_p = zeros_of_rows.copy()
    zeros_of_columns_p = zeros_of_columns.copy()

    assignments = []
   
    minimum_in_rows , index_of_min_in_rows  = find_min_length(zeros_of_rows_p)
    
    # remove the rows that have one zeros
    while (index_of_min_in_rows != -1):
        # print(zeros_of_rows_p)
        if (len(minimum_in_rows) > 0):
            c_index = minimum_in_rows[0]
            zeros_of_columns_p[c_index].clear()
            v = zeros_of_rows_p[index_of_min_in_rows].pop()
            assignments.append( ( index_of_min_in_rows, v ) )
            for j in range(len(zeros_of_rows_p)):
                zeros_of_rows_p[j] = list(filter(lambda x: x != v, zeros_of_rows_p[j])) 
        minimum_in_rows , index_of_min_in_rows  = find_min_length(zeros_of_rows_p)
        
        
    # print(zeros_of_rows_p, zeros_of_columns_p)
    return assignments

def min_in_graph(G, horizental_lines, vertical_lines):
    min = sys.maxsize
    min_row_index = -1
    min_column_index = -1
    for i in range(len(G)):

        for j in range(len(G)):
            if (G[i][j] > 0 and i not in horizental_lines and j not in vertical_lines and min > G[i][j]):
                min = G[i][j]
                min_row_index = i
                min_column_index = j

    return min, min_row_index, min_column_index 

def subtract_min_from_graph(G,min, horizental_lines, vertical_lines,zeros_of_rows,zeros_of_columns):
    
    for i in range(len(G)):
        for j in range(len(G)):
            if (G[i][j] > 0 and i not in horizental_lines and j not in vertical_lines):
                 x = G[i][j] - min
                 #print(G[i][j])
                 if x == 0 and G[i][j] != 0:
                     #print("row[",i,"] =  ",j)
                     zeros_of_rows[i].append(j)
                     zeros_of_columns[j].append(i) 
                 G[i][j] = x
            elif i in horizental_lines and j in vertical_lines :
                G[i][j] = G[i][j] + min
    return G, zeros_of_rows, zeros_of_columns

    def assign(zeros_of_rows,zeros_of_columns):
        for i in range(len(zeros_of_rows)):
            v = zeros_of_rows[i]               
if __name__ == '__main__':

    # http://www.hungarianalgorithm.com/examplehungarianalgorithm.php

    G = [[82, 83, 69, 92],
         [77, 37, 49, 92],
         [11, 69, 5, 86],
         [ 8,  9, 98, 23]] 
    # https://github.com/benchaplin/hungarian-algorithm
    G = [[22, 14, 120, 21, 4, 51],
         [19, 12, 172, 21, 28, 43],
         [161, 122, 2, 50, 128, 39],
         [19, 22, 90, 11, 28, 4],
         [1, 30, 113, 14, 28, 86],
         [60, 70, 170, 28, 68, 104]]    

    G1 =  len(G)*[]
    zeros_of_columns = len(G)*[] 
    zeros_of_rows = len(G)*[]
    que = queue.Queue()
    for i in range(len(G)):

        #zeros_of_rows.append([])
        zeros_of_columns.append([])    
        G1.append(G[i].copy())
    print(G1)

    
    p = 2 
    threads_of_rows = []
    threads_of_columns = []
    d = int(len(G) / p)
    #print(d)
    
    for i in range(p):
        start = i*d
        Gk = G1[start : start + d]
        #print(Gk)
        x = threading.Thread(target=lambda q, arg1: q.put(subtract_min_from_rows(arg1)), args=(que, Gk))  
        threads_of_rows.append(x)

    for i in range(len(threads_of_rows)):
        #print("start threads_of_rows ",i)

        threads_of_rows[i].start()

    for i in range(len(threads_of_rows)):
        # print("join")
        threads_of_rows[i].join()   

    # Check thread's return value

    result =[]
   
    
    print("Now merge rows")

    index = 0
    while not que.empty():
        returned_variables = que.get()
        g =  returned_variables[0]

        r = returned_variables[1]
        c = returned_variables[2]
        #print("r",r)
        #print("c", c)
        

        zeros_of_rows = zeros_of_rows + r
        #print("zers", zeros_of_columns)
        for i in range(len(c)):
            for j in range(len(c[i])):
                zeros_of_columns[i].append( c[i][j] + (index*d) )
        index = index + 1   
        result = result + g
        #G[index] = g
    G1 = result
    print(G1, zeros_of_rows, zeros_of_columns)
    #print(zeros_of_rows)
    #rint(zeros_of_columns)
    for i in range(p):
        Gk = []
        #print(i)
        for k in range(len(G1)):

            Gk.append([])
            s = i*d
            for j in range(d):
                
                v = G1[k][s+j]
                #print(v)
                Gk[k].append(v)
        #print("GK",Gk)
        x = threading.Thread(target=lambda q, arg1: q.put(subtract_min_from_columns(arg1)), args=(que, Gk))  
        threads_of_columns.append(x)

    for i in range(len(threads_of_columns)):
        #print("start threads_of_columns ",i)
        threads_of_columns[i].start()
    #threads_of_columns[1].start()
    #threads_of_columns[0].join()

    for i in range(len(threads_of_columns)):
        #print("join")
        threads_of_columns[i].join()      
    
    result = []
    print("Now merge columns")
    index = 0
    for k in range(len(G1)):
        result.append([])
   
    while not que.empty():
        returned_variables = que.get()
        g =  returned_variables[0]
        r =  returned_variables[1]
        c =  returned_variables[2]
        #print("r",r)
        #print("c", c)
        #print("zeros of rows",zeros_of_rows)
        #print("zeros of columns",zeros_of_columns)
        #print("g",g)
        for i in range(len(g)):
            
            for j in range(len(g[i])):
                result[i].append(g[i][j])
        for i in range(len(c)):
            for j in range(len(c[i])):
                zeros_of_columns[i+(index*d)].append(c[i][j])
        
        for i in range(len(r)):
            for j in range(len(r[i])):
               # print("asa ",r[i][j], "i ", i, "j ", j, "index ", index)
                zeros_of_rows[i].append(r[i][j] + (index*d))
        index = index + 1
    print(result, zeros_of_rows, zeros_of_columns)
    G1 = result
    #print(G1)

    for i in range(len(zeros_of_rows)):
        r.append([])
        for j in range(len(zeros_of_rows[i])):
            r[i].append(zeros_of_rows[i][j])

    for i in range(len(zeros_of_columns)):
        c.append([])
        for j in range(len(zeros_of_columns[i])):
            c[i].append(zeros_of_columns[i][j])
        
    number_of_lines,horizental_lines,vertical_lines = cover_zeros(r, c)
    
    # print(zeros_of_rows,zeros_of_columns)
    
    # print("number of lines",number_of_lines, horizental_lines ,vertical_lines )
    
    # print(zeros_of_columns)
    min, row_index, column_index = min_in_graph(G1,horizental_lines,vertical_lines)

    # print("G[ ",row_index," ][ ",column_index," ] = ",min)

    #intersections = []
    
    #for i in range(len(horizental_lines)):
    #    for j in range(len(vertical_lines)):
    #        intersections.append((horizental_lines[i],vertical_lines[j]))
    
    # print(intersections)

    if (number_of_lines != len(G1)):
        match, zeros_of_rows,zeros_of_columns = subtract_min_from_graph(G1,min,horizental_lines,vertical_lines,zeros_of_rows,zeros_of_columns)

        # print(match, zeros_of_rows,zeros_of_columns)        

        r = []
        c = []
        
        for i in range(len(zeros_of_rows)):
            r.append([])
            for j in range(len(zeros_of_rows[i])):
                r[i].append(zeros_of_rows[i][j])

        for i in range(len(zeros_of_columns)):
            c.append([])
            for j in range(len(zeros_of_columns[i])):
                c[i].append(zeros_of_columns[i][j])
            
        number_of_lines,horizental_lines,vertical_lines = cover_zeros(r, c)

    # print("number of lines",number_of_lines, horizental_lines ,vertical_lines )
    
    if (number_of_lines == len(G1)):
        assignments = assign_tasks_to_workers(zeros_of_rows, zeros_of_columns)
        print("assignemt",assignments)    
    for k in range(len(assignments)):
        i = assignments[k][0]
        j = assignments[k][1]
        print("worker", i, " has task  ", j, " whose weight is  ", G[i][j])

   

   
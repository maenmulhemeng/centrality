
import testGraph as example1
#import hugeGraph as example2 
import paralleGraph as example3
#from collections import deque # queue

#import logging
#import threading
#import queue
import sys
import time
import huge_matrix as hm

def get_min_from_row(G,row):
    min = sys.maxsize
    index = -1
    for i in range(len(G)):
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

def subtract_min_from_rows(G,zeros_of_rows,zeros_of_columns ):
    
    for row in range(len(G)):
        min,_ = get_min_from_row(G,row)
        for column in range(len(G[row])):
            x = G[row][column] - min
            # print(x)
            if x == 0 and G[row][column] != 0:
                # print("row[",row,"] =  ",column)
                zeros_of_rows[row][column] = 1
                zeros_of_columns[column][row] = 1 
           
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

def subtract_min_from_columns(G,zeros_of_rows,zeros_of_columns ):
    
    for column in range(len(G)):
        min,_ = get_min_from_column(G, column)
        for row in range(len(G)):
            x = G[row][column] - min
            
            if x == 0 and G[row][column]!=0:
                zeros_of_rows[row][column] = 1
                zeros_of_columns[column][row] = 1 
            G[row][column] = x
    return G, zeros_of_rows,zeros_of_columns
def validate_zeros(zeros_of_rows, zeros_of_columns):
    for i in range(len(zeros_of_rows)):
        for j in range(len(zeros_of_rows[i])):
            x = zeros_of_rows[i][j]
            if i  not in zeros_of_columns[x]:
                return False
    for i in range(len(zeros_of_columns)):
        for j in range(len(zeros_of_columns[i])):
            x = zeros_of_columns[i][j]
            if i not in zeros_of_rows[x]:
                return False
    return True
def cover_zeros(zeros_of_rows_p, zeros_of_columns_p):
   

    number_of_lines = 0
    maximum_in_rows = max(zeros_of_rows_p, key = lambda x:len(x))
    index_of_max_in_rows = zeros_of_rows_p.index(maximum_in_rows)

    maximum_in_columns = max(zeros_of_columns_p, key = lambda x:len(x))
    index_of_maximum_in_columns = zeros_of_columns_p.index(maximum_in_columns)
    
    horizental_lines = []
    vertical_lines = []
    while (maximum_in_rows != {} and maximum_in_columns != {}): ## O(n)
        #print(maximum_in_rows)
        #print(maximum_in_columns)
        #print(zeros_of_rows_p,zeros_of_columns_p)
        #print("-----------------------------------")
        if (len(maximum_in_rows) >= len(maximum_in_columns)):
            horizental_lines.append(index_of_max_in_rows)
            for i in zeros_of_rows_p[index_of_max_in_rows]: ## O(k)
                #index = zeros_of_rows_p[index_of_max_in_rows][i]    
                zeros_of_columns_p[i].pop(index_of_max_in_rows) ## O(1)
            zeros_of_rows_p[index_of_max_in_rows] = {}
        else:
            vertical_lines.append(index_of_maximum_in_columns)
            for i in zeros_of_columns_p[index_of_maximum_in_columns]:
                #index = zeros_of_columns_p[index_of_maximum_in_columns][i]
                zeros_of_rows_p[i].pop(index_of_maximum_in_columns)
            zeros_of_columns_p[index_of_maximum_in_columns] = {}
            
        maximum_in_rows = max(zeros_of_rows_p, key = lambda x:len(x))
        index_of_max_in_rows = zeros_of_rows_p.index(maximum_in_rows)

        maximum_in_columns = max(zeros_of_columns_p, key = lambda x:len(x))
        index_of_maximum_in_columns = zeros_of_columns_p.index(maximum_in_columns)

        
        number_of_lines = number_of_lines + 1   
    return number_of_lines , horizental_lines, vertical_lines
    
def assign_tasks_to_workers(zeros_of_rows_p, zeros_of_columns_p):
    #print(zeros_of_rows,zeros_of_columns)
    

    assignments = []
   
    minimum_in_rows , index_of_min_in_rows  = find_min_length(zeros_of_rows_p)
    
    # remove the rows that have one zeros
    while (index_of_min_in_rows != -1):
        #print(zeros_of_rows_p, minimum_in_rows)
        if (len(minimum_in_rows) > 0):
            c_index = list(minimum_in_rows.keys())[0]
            #print("first ", first_element)
            #c_index = minimum_in_rows[first_element]
            zeros_of_columns_p[c_index].clear()
            v = zeros_of_rows_p[index_of_min_in_rows].pop(c_index)
            zeros_of_rows_p[index_of_min_in_rows].clear()
            assignments.append( ( index_of_min_in_rows, c_index ) )
            for j in range(len(zeros_of_rows_p)):
                
                try:
                    zeros_of_rows_p[j].pop(c_index)
                except:
                    1+1
                    #print("has no", c_index)
                #print(zeros_of_rows_p[j],c_index)
        minimum_in_rows , index_of_min_in_rows  = find_min_length(zeros_of_rows_p)
        
        
    #print(zeros_of_rows_p, zeros_of_columns_p)
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
                     zeros_of_rows[i][j] = 1
                     zeros_of_columns[j][i] = 1 
                 G[i][j] = x
            elif i in horizental_lines and j in vertical_lines :
                if (G[i][j] == 0):
                    zeros_of_columns[j].pop(i)
                    zeros_of_rows[i].pop(j)
                G[i][j] = G[i][j] + min
    return G, zeros_of_rows, zeros_of_columns

def sequential_hungarain(G):
    start_time = time.time()
    performance = {}
    #G1 =  len(G)*[]
    zeros_of_columns = len(G)*[] 
    zeros_of_rows = len(G)*[]
    
    for i in range(len(G)):
        zeros_of_rows.append({})
        zeros_of_columns.append({})    
        #G1.append(G[i].copy())
    #print(G1)
    performance["init"] = (time.time() - start_time)
    start_time = time.time()
    
    match, zeros_of_rows, zeros_of_columns = subtract_min_from_rows(G, zeros_of_rows, zeros_of_columns ) 
    
    performance["subtract_min_from_rows"] = (time.time() - start_time)
    
    start_time = time.time()
    # print(match,zeros_of_rows,zeros_of_columns)
    #print (validate_zeros(zeros_of_rows, zeros_of_columns))
    match, zeros_of_rows, zeros_of_columns = subtract_min_from_columns(G,zeros_of_rows,zeros_of_columns )        
    performance["subtract_min_from_columns"] = (time.time() - start_time)

    start_time = time.time()
    #print(match,zeros_of_rows,zeros_of_columns)
    r = []
    c = []
    
    for i in range(len(zeros_of_rows)):
        r.append({})
        for j in zeros_of_rows[i]:
            r[i][j] = 1

    for i in range(len(zeros_of_columns)):
        c.append({})
        for j in zeros_of_columns[i]:
            c[i][j] = 1
        
    number_of_lines,horizental_lines,vertical_lines = cover_zeros(r, c)
    #print("number of lines",number_of_lines, horizental_lines ,vertical_lines )
    while (number_of_lines != len(G)):
        min, row_index, column_index = min_in_graph(G,horizental_lines,vertical_lines)
        #print("G[ ",row_index," ][ ",column_index," ] = ",min)

        match, zeros_of_rows,zeros_of_columns = subtract_min_from_graph(G,min,horizental_lines,vertical_lines,zeros_of_rows,zeros_of_columns)

        #print(match, zeros_of_rows,zeros_of_columns)        

        r = []
        c = []
        
        for i in range(len(zeros_of_rows)):
            r.append({})
            for j in zeros_of_rows[i]:
                r[i][j] = 1

        for i in range(len(zeros_of_columns)):
            c.append({})
            for j in zeros_of_columns[i]:
                c[i][j] = 1
            
        number_of_lines,horizental_lines,vertical_lines = cover_zeros(r, c)

        #print("number of lines",number_of_lines, horizental_lines ,vertical_lines )
    
    if (number_of_lines == len(G)):
        assignments = assign_tasks_to_workers(zeros_of_rows, zeros_of_columns)
        #print("assignemt",assignments)    

    performance["rest"] = (time.time() - start_time)
    return assignments, performance
if __name__ == '__main__':
    start_time = time.time()
    # http://www.hungarianalgorithm.com/examplehungarianalgorithm.php
    #G = [[82, 83, 69, 92],
    #     [77, 37, 49, 92],
    #     [11, 69, 5, 86],
    #     [ 8,  9, 98, 23]] 
    # https://github.com/benchaplin/hungarian-algorithm
    #G = [[22, 14, 120, 21, 4, 51],
    #     [19, 12, 172, 21, 28, 43],
    #     [161, 122, 2, 50, 128, 39],
    #     [19, 22, 90, 11, 28, 4],
    #     [1, 30, 113, 14, 28, 86],
    #     [60, 70, 170, 28, 68, 104]]  
    #G = [[5,	8,	47,	49,	33],
    #     [88,	79,	46,	23,	4],
    #     [75,	17,	1,	34,	55],
    #     [98,	74,	90,	41,	68],
    #     [12,	67,	43,	32,	51]]
    G = [[5,    8,	 47, 49,	33,	 34,  45,	34,	 54,    59],
         [88,   79,	 46, 23,	4,	 54,  321,  54,	 85,    43],
         [75,	17,	 1,	 34,	55,	 234, 2,    58,	 654,   59],
         [98,	74,	 90, 41,	68,	 12,  1,	13,	 466,	52],
         [12,	67,	 43, 32,	51,	 890, 59,   85,	 76,	37],
         [890,	90,	 89, 89,	808, 9,   34,	674, 56,	52],
         [89,	8,	 3,	 890,	34,	 8,	  378,	65,	 85,	36],
         [323,	123, 49, 959,	49,	 3,	  8,	95,	 36,	74],
         [3,	2,	 23, 54,	59,	 76,  65,	54,	 559,	5 ],
         [6,	54,	 45, 95,	59,	 87,  90,	237, 23,	232]]
    G1 =[]
    #G = hm.huge_matrix(200,200)
    for i in range(len(G)):
        G1.append([])
        for j in range(len(G[i])):
            G1[i].append(G[i][j])
    print("Matrix was copied")
    
    assignments,performance = sequential_hungarain(G1)  

    for k in range(len(assignments)):
        i = assignments[k][0]
        j = assignments[k][1]
        print("worker", i, " has task  ", j, " whose weight is  ", G[i][j])
    print("--- %s seconds ---" % (time.time() - start_time))
    for k in performance:
        print (k, performance[k])
 


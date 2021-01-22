from mpi4py import MPI
import time
import sys
def get_min_from_row(G,row):
    #print(G[row])
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


def subtract_min_from_rows(G, zeros_of_rows,zeros_of_columns):
    
    for row in range(len(G)):
        minimum,_ = get_min_from_row(G,row) 
        #zeros_of_rows.append({})
        for column in range(len(G[row])):
            #print(minimum)
            x = G[row][column] - minimum
            # print(x)
            if x == 0 and G[row][column] != 0:
                #print("row[",row,"] =  ",column)

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

def subtract_min_from_columns(G,minimum_in_columns,zeros_of_rows,zeros_of_columns):
    #print(zeros_of_columns)
    for column in range(len(G[0])):
        for row in range(len(G)):
            x = G[row][column] - minimum_in_columns[column]
            
            if x == 0 and G[row][column]!=0:
                #print("row[",row,"] =  ",column)
                zeros_of_rows[row][column] = 1
                zeros_of_columns[column][row] = 1 
            G[row][column] = x
    #print(zeros_of_columns)
    return G, zeros_of_rows,zeros_of_columns
def cover_zeros(zeros_of_rows_p, zeros_of_columns_p):
    #zeros_of_rows_p = zeros_of_rows.copy()
    #zeros_of_columns_p = zeros_of_columns.copy()

    
    number_of_lines = 0
    maximum_in_rows = max(zeros_of_rows_p, key = lambda x:len(x))
    index_of_max_in_rows = zeros_of_rows_p.index(maximum_in_rows)

    maximum_in_columns = max(zeros_of_columns_p, key = lambda x:len(x))
    index_of_maximum_in_columns = zeros_of_columns_p.index(maximum_in_columns)
    
    horizental_lines = []
    vertical_lines = []
    #print("start")
    while (maximum_in_rows != {} and maximum_in_columns != {}):
        #print(index_of_max_in_rows, maximum_in_rows, index_of_maximum_in_columns, maximum_in_columns)
        
        #print(maximum_in_rows,maximum_in_columns)
        if (len(maximum_in_rows) >= len(maximum_in_columns)):
            horizental_lines.append(index_of_max_in_rows)
            for i in zeros_of_rows_p[index_of_max_in_rows]:
                #print(zeros_of_columns_p[i],index_of_max_in_rows)
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
      
        if (len(minimum_in_rows) > 0):
            c_index = list(minimum_in_rows.keys())[0]
           
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
        for j in range(len(G[i])):
            
            if (G[i][j] > 0 and i not in horizental_lines and j not in vertical_lines and min > G[i][j]):
                #print(G[i][j],i,j,horizental_lines,vertical_lines)
                min = G[i][j]
                min_row_index = i
                min_column_index = j
            

    return min, min_row_index, min_column_index 

def subtract_min_from_graph(G,min, horizental_lines, vertical_lines,zeros_of_rows,zeros_of_columns):
    
    for i in range(len(G)):
        for j in range(len(G[i])):
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
                    #print("row[",i,"] =  ",j)
                    zeros_of_columns[j].pop(i)
                    zeros_of_rows[i].pop(j)
                G[i][j] = G[i][j] + min
    return G, zeros_of_rows, zeros_of_columns

G_original = [[5,    8,	 47, 49,	33,	 34,  45,	34,	 54,    59],
         [88,   79,	 46, 23,	4,	 54,  321,  54,	 85,    43],
         [75,	17,	 1,	 34,	55,	 234, 2,    58,	 654,   59],
         [98,	74,	 90, 41,	68,	 12,  1,	13,	 466,	52],
         [12,	67,	 43, 32,	51,	 890, 59,   85,	 76,	37],
         [890,	90,	 89, 89,	808, 9,   34,	674, 56,	52],
         [89,	8,	 3,	 890,	34,	 8,	  378,	65,	 85,	36],
         [323,	123, 49, 959,	49,	 3,	  8,	95,	 36,	74],
         [3,	2,	 23, 54,	59,	 76,  65,	54,	 559,	5 ],
         [6,	54,	 45, 95,	59,	 87,  90,	237, 23,	232]]
G = []
#G = hm.huge_matrix(200,200)
for i in range(len(G_original)):
    G.append([])
    for j in range(len(G_original[i])):
        G[i].append(G_original[i][j])


p = 2
distribute_command = 'distribute_command'
distrubute_minimum_in_columns_command = 'distrubute_minimum_in_columns'
distribute_cover_lines_command = 'distribute_cover_lines_command'
distribute_global_minimum_command = 'distribute_global_minimum_command'
return_miminum_in_columns =  'return_miminum_in_columns'
return_matrix =  'return_matrix'
return_global_minimum = 'return_global_minimum'

tags= {}
tags[distribute_command] = 1
tags[return_miminum_in_columns] = 2
tags[distrubute_minimum_in_columns_command] = 3
tags[return_matrix] = 4
tags[distribute_cover_lines_command] = 5
tags[return_global_minimum] = 6
tags[distribute_global_minimum_command] = 7

zeros_of_columns = len(G)*[] 
zeros_of_rows = len(G)*[]




for i in range(len(G)):
    zeros_of_rows.append({})
    zeros_of_columns.append({})   
if (p > len(G)):
        p = len(G)

d = int(len(G) / p)
if len(G) % 2 != 0 :
    #print("new thread was added because the dimention of the adjacency matrix is an odd number")
    p = p +1
    #print(d)

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    #print("launch ",rank )
    start_time = time.time()
    performance = {}
    #G1 =  len(G)*[]
    
    
    
    
    performance["init"] = (time.time() - start_time)
    start_time = time.time()
    
    #print(G)
    for i in range(1,p):  # O(p)
        start = i*d
        Gk = G[start : start + d]
        n = d
        if i + 1 == p:
            n = len(G) - (i * d)
            Gk = G[start : ]
        #print(Gk)

        comm.send(Gk, dest=i, tag=tags[distribute_command])
    
    G1 = G[0 : d]

    #print("Will process",G1)
    subtract_min_from_rows(G1,zeros_of_rows,zeros_of_columns)

   
    returned_miminum_in_columns = []  
    local_minimum_in_columns = [] 
    for j in range(len(G1[0])):
        min, _ = get_min_from_column(G1,j)
        local_minimum_in_columns.append(min)
    
    returned_miminum_in_columns.append(local_minimum_in_columns)
    #print("after subtraction ",G1)
    
    for i in range(1,p):
        returned_miminum_in_columns.append(comm.recv(source=i, tag=tags[return_miminum_in_columns]))
    
    performance["subtract_min_from_rows"] = (time.time() - start_time)
    
    start_time = time.time()

    #print("recieved ", returned_miminum_in_columns)

    minimum_in_columns = []
    for j in range(len(returned_miminum_in_columns[0])):
        min, _ = get_min_from_column(returned_miminum_in_columns,j)
        minimum_in_columns.append(min)  

    #print("found minimum ", minimum_in_columns)
    
    for i in range(1,p):
        comm.send(minimum_in_columns, dest=i, tag=tags[distrubute_minimum_in_columns_command])

    subtract_min_from_columns(G1,minimum_in_columns,zeros_of_rows,zeros_of_columns)
    
    
    global_zeros_of_columns = len(G)*[] 
    global_zeros_of_rows = len(G)*[] 

    for i in range(len(zeros_of_rows)):
        global_zeros_of_rows.append({})
        for j in zeros_of_rows[i]:
            global_zeros_of_rows[i][j] = 1

    for i in range(len(zeros_of_columns)):
        global_zeros_of_columns.append({})
        for j in zeros_of_columns[i]:
            global_zeros_of_columns[i][j] = 1

    for i in range(1,p):
        Gk,r,c = comm.recv(source=i, tag=tags[return_matrix])
        for k in range(len(Gk)):
            G1.append(Gk[k])
        
        count = 0 
        for k in r:
            #print(k)
            for cc in k:
                index = (d*i) + count 
                #print(c,index)
                global_zeros_of_rows[index][cc] = 1
            count = count + 1
        
        count = 0
        for k in c:
            for r in k:
                #print(r)
                index = (d*i) + r 
                global_zeros_of_columns[count][index] = 1 
            count = count + 1
    #print("hello",G1,zeros_of_rows,zeros_of_columns)

    performance["subtract_min_from_columns"] = (time.time() - start_time)

    start_time = time.time()
   
    
    #print(zeros_of_rows,zeros_of_columns)  
    number_of_lines,horizental_lines,vertical_lines = cover_zeros(global_zeros_of_rows, global_zeros_of_columns)
    #print("number of lines",number_of_lines, horizental_lines ,vertical_lines )
    #print("let's loop")
    while (number_of_lines != len(G1)):
        
        #print(G)
        for i in range(1,p):  # O(p)
            start = i*d
            hk = [number-(i*d) for number in horizental_lines if  (start <= number)  and (number < start+d)]
            
            #print("there",hk,vertical_lines)
        
            comm.send((hk,vertical_lines,number_of_lines) , dest=i, tag=tags[distribute_cover_lines_command])
        
        G1 = G[0: d]
        hlines = [number for number in horizental_lines if  (0 <= number)  and (number < d)]
        min, row_index, column_index = min_in_graph(G1, hlines,vertical_lines)
        for i in range(1,p):
            returned_min = comm.recv(source=i, tag=tags[return_global_minimum])
            #print("returned_min",returned_min, " min ",min)
            if returned_min < min:
                min = returned_min
        
        #print("G[ ",row_index," ][ ",column_index," ] = ",min)
        for i in range(1,p):  # O(p)
            comm.send(min, dest=i, tag=tags[distribute_global_minimum_command])
        #print("asd ",hlines,vertical_lines)
        G1, zeros_of_rows,zeros_of_columns = subtract_min_from_graph(G1,min,hlines,vertical_lines,zeros_of_rows,zeros_of_columns)
        #print(G1, zeros_of_rows,zeros_of_columns)
        
        global_zeros_of_columns =len(G)*[] 
        global_zeros_of_rows = len(G)*[] 

        for i in range(len(zeros_of_rows)):
            global_zeros_of_rows.append({})
            for j in zeros_of_rows[i]:
                global_zeros_of_rows[i][j] = 1

        for i in range(len(zeros_of_columns)):
            global_zeros_of_columns.append({})
            for j in zeros_of_columns[i]:
                global_zeros_of_columns[i][j] = 1

        for i in range(1,p):
            Gk,r,c = comm.recv(source=i, tag=tags[return_matrix])
            for k in range(len(Gk)):
                G1.append(Gk[k])
            
            count = 0 
            for k in r:
                #print(k)
                for cc in k:
                    index = (d*i) + count 
                    #print(c,index)
                    global_zeros_of_rows[index][cc] = 1
                count = count + 1
            
            count = 0
            for k in c:
                for r in k:
                    #print(r)
                    index = (d*i) + r 
                    global_zeros_of_columns[count][index] = 1 
                count = count + 1
            #print("hello",G1,zeros_of_rows,zeros_of_columns)


        #print(G1,global_zeros_of_rows, global_zeros_of_columns)        

        r = [] 
        c = [] 

        for i in range(len(global_zeros_of_rows)):
            r.append({})
            for j in global_zeros_of_rows[i]:
                r[i][j] = 1

        for i in range(len(global_zeros_of_columns)):
            c.append({})
            for j in global_zeros_of_columns[i]:
                c[i][j] = 1

        #print(G1)      
        number_of_lines,horizental_lines,vertical_lines = cover_zeros(r, c)
        #print(G1)
        #print("number of lines",number_of_lines, horizental_lines ,vertical_lines )
    
    # let's stop all of the children by sending them the number of the covering lines
    for i in range(1,p):  # O(p)
            comm.send(([],[],number_of_lines) , dest=i, tag=tags[distribute_cover_lines_command])

    if (number_of_lines == len(G1)):
        assignments = assign_tasks_to_workers(global_zeros_of_rows, global_zeros_of_columns)
        #print("assignemt",assignments)    

    performance["rest"] = (time.time() - start_time)
    
    #print("let's assign")
    for k in range(len(assignments)):
        i = assignments[k][0]
        j = assignments[k][1]
        print("worker", i, " has task  ", j, " whose weight is  ", G_original[i][j])
    print("--- %s seconds ---" % (time.time() - start_time))
    for k in performance:
        print (k, performance[k])
else:
    #print("launch ",rank )
    G = comm.recv(source=0, tag=tags[distribute_command])

    subtract_min_from_rows(G,zeros_of_rows,zeros_of_columns)

    #print(G,zeros_of_rows,zeros_of_columns)

    minimum_in_columns = []
    for j in range(len(G[0])):
        min, _ = get_min_from_column(G,j)
        minimum_in_columns.append(min)
    #print(minimum_in_columns)

    comm.send(minimum_in_columns, dest=0, tag=tags[return_miminum_in_columns])

    minimum_in_columns = comm.recv(source=0, tag=tags[distrubute_minimum_in_columns_command])

    #print("received minimum_in_columns ",minimum_in_columns)

    subtract_min_from_columns(G,minimum_in_columns,zeros_of_rows,zeros_of_columns)

   
    comm.send((G,zeros_of_rows,zeros_of_columns), dest=0, tag=tags[return_matrix])

    hlines,vlines,number_of_lines  = comm.recv(source=0, tag=tags[distribute_cover_lines_command])
    
    while(number_of_lines != len(G[0])):
        min, row_index, column_index = min_in_graph(G,hlines,vlines)
        
        comm.send(min , dest=0, tag=tags[return_global_minimum])
        #print("here", hlines, vlines)
        

        min = comm.recv(source=0, tag=tags[distribute_global_minimum_command])
        
        #print("here",min)
        
        G, zeros_of_rows,zeros_of_columns = subtract_min_from_graph(G,min,hlines,vlines,zeros_of_rows,zeros_of_columns)
        
         #print(G,zeros_of_rows,zeros_of_columns)

        comm.send((G,zeros_of_rows,zeros_of_columns), dest=0, tag=tags[return_matrix])

        hlines,vlines,number_of_lines = comm.recv(source=0, tag=tags[distribute_cover_lines_command])

        if (number_of_lines == len(G[0])):
            break
        print(hlines,vlines,number_of_lines)

        #mpirun -n 2 python mpi_hungarain.py 
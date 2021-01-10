import sequential_hungarian as seq
import multithreading_hungarian as as_threads
import multiprocessing_hungarian_with_manager as as_manager
import multiprocessing_hungarian_ctype as as_processes
import multiprocessing as mp

import time
import huge_matrix as hm

if __name__ == '__main__':
    
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
  for i in range(1):
    print("")   
    print ("Test No ", i+1)   
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
    G2 = []
    n = 200
    p_threads = 50
    p_processes = 5

    #G = hm.huge_matrix(n,n)

    manager = mp.Manager()
    arr = manager.list()

   

    for i in range(len(G)):
        G1.append([])
        G2.append([])
        arr.append(manager.list(G[i]))      
        for j in range(len(G[i])):
            G1[i].append(G[i][j])
            G2[i].append(G[i][j])
    print("matrix was copied of dimension ",len(G)) 
   
    start_time = time.time()
    b , performance_of_seq =  seq.sequential_hungarain(G1)
    seq_time = (time.time() - start_time)
   
    
    print("The number of threads ", p_threads)
    start_time = time.time()
    a, performance_of_threads =  as_threads.parallel_hungarian(G, p_threads)
    parallel_time = (time.time() - start_time)


    print("The number of processes (with manager) ", p_processes)
    start_time = time.time()
    a, performance_of_processes =  as_manager.parallel_hungarian(arr, p_processes)
    dist_time = (time.time() - start_time)



    print("The number of processes (ctype) ", p_processes)
    start_time = time.time()

    a, performance_of_ctype =  as_processes.parallel_hungarian(G2, p_processes)
    dist_ctype_time = (time.time() - start_time)

    print("----- Time ---------") 
    print("--- Seq time is %s seconds ---" % seq_time)
    
    print("---  Multi-Threading time is %s seconds ---" % parallel_time)

    print("--- Multi-processing (with manager) is %s seconds ---" % dist_time)

    print("--- Multi-processing (with ctype) is %s seconds ---" % dist_ctype_time)
    
    print("----- Performance ---------- ")
    if (dist_time != 0 ):
     print("--- Performace time in terms of multithreading is %s  ---" % (seq_time/parallel_time))
     print("--- Performace time in terms of multiprocessing (with manager) is %s  ---" % (seq_time/dist_time))
     print("--- Performace time in terms of multiprocessing (ctype) is %s  ---" % (seq_time/dist_ctype_time))
    else:
     print("--- The parallel version time is almose zero") 

    print("-------- Performance details -------------") 
    for k in performance_of_seq:
     print (k, " in threads ", performance_of_threads[k])
     print (k, " in processes (with manager)", performance_of_processes[k])
     print (k," in ctype ", performance_of_ctype[k])
     print (k," in seq ", performance_of_seq[k])

       
 


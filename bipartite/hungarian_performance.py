import sequential_hungarian as seq
import parallel_hungarian as parallel
import time

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
  for i in range(10):
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
    
    start_time = time.time()
    b , performance_of_seq =  seq.sequential_hungarain(G)
    seq_time = (time.time() - start_time)
   
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

    start_time = time.time()
    a, performance_of_parallel =  parallel.parallel_hungarian(G, 2)
    dist_time = (time.time() - start_time)

    print("--- Seq time is %s seconds ---" % seq_time)
    
    print("--- Dist time is %s seconds ---" % dist_time)
    if (dist_time != 0 ):
     print("--- Performace time is %s  ---" % (seq_time/dist_time))
    else:
     print("--- The parallel version time is almose zero") 

    for k in performance_of_parallel:
        print (k, " in parallel ", performance_of_parallel[k]," in seq " , performance_of_seq[k])


 

from __future__ import print_function
from multiprocessing import sharedctypes
import multiprocessing
import ctypes
import numpy as np

def shared_array(shape):
    """
    Form a shared memory numpy array.
    
    http://stackoverflow.com/questions/5549190/is-shared-readonly-data-copied-to-different-processes-for-python-multiprocessing 
    """
    
    #X = np.random.random(shape)
    
    return shared_array


def parallel_function(i,j,X_shape, array):
    X_np = np.frombuffer(array, dtype=np.float64).reshape(X_shape)
        
    X_np[i][j]=X_np[i][j]+3 

if __name__ == '__main__':
    """
    The processing pool needs to be instantiated in the main 
    thread of execution. 
    """
    X_shape = (10, 10)
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
    # Randomly generate some data
    data = np.array(G)
    X = multiprocessing.RawArray('d', X_shape[0] * X_shape[1])
    X_np = np.frombuffer(X).reshape(X_shape)
    # Copy data to our shared array.
    np.copyto(X_np, data)

    print(type(X),type(X_np))
    p = []
    n = 2

        
    for i in range(n):
        p.append(multiprocessing.Process(target=parallel_function, args=(i,i,X_shape, X)))
    for i in range(n):
        p[i].start()
    for i in range(n):
        p[i].join()
    
    print(X[11])
    print("finish")
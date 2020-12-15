import logging
import threading
import time

mutex = threading.Lock()

shared_variable = 0
def thread_function(name):
    global shared_variable
    global mutex
    logging.info("Thread %s: starting", name)
    logging.info("Thread %s :shared variable %s", name , shared_variable)
    mutex.acquire()
    shared_variable = shared_variable +1
    mutex.release()
    logging.info("Thread %s : becomes %s", name , shared_variable)
    logging.info("Thread %s: finishing", name)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    logging.info("Main    : before creating thread")
    n = 5
    A = []
    for i in range(n):
        A.append(threading.Thread(target=thread_function, args=(i,)))
    for i in range(n):
        A[i].start()

    for i in range(n):
        A[i].join()
    
    logging.info("main :shared variable %s", shared_variable)
    
    logging.info("Main    : all done")

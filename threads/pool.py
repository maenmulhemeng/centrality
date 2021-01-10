from time import sleep
import concurrent.futures
import threading
import time

def count_number_of_words(sentence):
    number_of_words = len(sentence.split())
    sleep(1)
    #print("asd")
    #print("Number of words in the sentence :\n",sentence," : {}".format(number_of_words),end="\n")
    return number_of_words

def with_pool(n,data):
    
    print("init")
    executor = concurrent.futures.ThreadPoolExecutor(n)
    print("let's go")
    #sleep(10)
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        threads = []
        for i in range(n):
            threads.append(executor.submit(count_number_of_words, (data)))
           
        for future in concurrent.futures.as_completed(threads):
            future.result()
            
def without_pool(n,data):
    threads = [] 
    for index in range(n):
        x = threading.Thread(target=count_number_of_words, args=(data,))
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        thread.join()
        
if __name__ == '__main__':
    sentence = "Python Multiprocessing is an important library for achieving parallel programming."
    n = 10
    start_time = time.time()
    with_pool(n,sentence)
    pool_time = (time.time() - start_time)
    
    start_time = time.time()
    without_pool(n,sentence)
    without_pool_time = (time.time() - start_time)

    start_time = time.time()
    for i in range(n):
        count_number_of_words(sentence)
    seq_time = (time.time() - start_time)


    print("pool time ",pool_time, " threads time ", without_pool_time, " seq time",seq_time)
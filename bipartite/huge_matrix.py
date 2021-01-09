import random

def huge_matrix(n,m,min=1,max=10000):
    a = []
    for i in range(n):
        a.append([])
        for j in range(m):
            a[i].append(random.randint(min, max))
    
    return a
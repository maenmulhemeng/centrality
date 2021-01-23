def convert_to_workers(G):
    w = []
    for i in range(len(G)):
        s = []
        for j in range(len(G[i])):
            s.append(( j , G[i][j]))
        s = sorted(s, key=lambda tup: tup[1])
        w.append(s)
                    
    return w
def convert_to_tasks(G):
    w = []
    for j in range(len(G[0])):
        s = []
        for i in range(len(G)):
            s.append(( i , G[i][j]))
        #s = sorted(s, key=lambda tup: tup[1])
        w.append(s)
                    
    return w

def average(G):
    sum = 0
    for i in range(len(G)):
        for j in range(len(G[i])):
            sum = sum + G[i][j]
    return sum / (len(G) * len(G[0]))

def prioroties(w,a):
    totals = []
    for i in range(len(w)):
        counter = 0
        for j in range(len(w[i])):
            if (w[i][j][1] <= a):
                counter = counter + 1
        totals.append((i,counter,w[i]))
    totals = sorted(totals, key=lambda tup:tup[1])
    return totals

def assign(w,t):
    assignments = {}
    for i in range(len(w)):
        for j,v in w[i][2]:
            if j not in assignments:
                assignments[j]  = (w[i][0], v) 
                print("worker ",w[i][0]," takes ", j )

                break
            else:
                print("worker ",w[i][0]," could not take ", j )
    return assignments
if __name__ == '__main__':

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
    a = average(G)
    #print(a)

    w = convert_to_workers(G)
    t = convert_to_tasks(G)

    w = prioroties(w,a)
    t = prioroties(t,a)
    #print(G)
    #print(t)
    assignments =  assign(w,t)
    print(assignments)
    for t in assignments:
        print("worker",assignments[t][0] , " has task  ", t, " whose weight is  ", assignments[t][1])
    

a = [[1,2],[0,1]]
b = [[1,2],[0,1]]

for indexi,i in enumerate(a):
    for indexj,j in enumerate(i):
        c = a[indexi][indexj] + b[indexi][indexj]
        print c
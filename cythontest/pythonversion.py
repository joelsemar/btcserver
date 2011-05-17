def run(array_1, array_2):
    for i in range(len(array_1)):
        a, b = array_1[i], array_2[i]
        a[0] += b[0]
        a[1] += b[1]
    

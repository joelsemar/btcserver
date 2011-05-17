cpdef int run(array_1, array_2):
    ret = []
    cdef int i = len(array_1)
    while i:
        arr_1 = array_1[i]
        arr_2 = array_2[i]
        a = arr_1[0]
        b = arr_2[0]
        c = arr_1[1]
        d = arr_2[1]
        ret.append([a+b, c+d])
        i -= 1
    return 0
    
    

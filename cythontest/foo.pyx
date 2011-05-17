cpdef int foo(int times):
    cdef list x = []
    for i in range(times):
        for j in range(10):
            x.append(i*j)
    return len(x)
		
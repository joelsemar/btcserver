import cythonversion
import pythonversion
import time
from random import choice



def testfunc(func, times=1000):
    p = range(17)
    array_1 = [[choice(p), choice(p)] for _ in range(100)]
    array_2 = [[choice(p), choice(p)] for _ in range(100)]
    init = time.time()
    for _ in range(times):
        func(array_1, array_2)
    
    return '%s seconds' % (time.time() - init)


def main_test(times=1000):
    print "Cython: %s" % testfunc(cythonversion.run, times)
    print "Python: %s" % testfunc(pythonversion.run, times)
    

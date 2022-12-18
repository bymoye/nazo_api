# cython: language_level=3
# distutils: language = c++

"""
@ Author : bymoye
@ createtime: 2022.1.21
@ engine: Storm
@ Modified from Pyewacket
"""
import itertools as _itertools
__all__ = (
    #"seed",
    "randbelow", "randint", "randrange",
    "shuffle", 
)


cdef extern from "Rand.hpp":
    cdef int uniform_int_variate "Storm::uniform_int_variate"(int a, int b)
    cdef int random_range "Storm::random_range"(int start, int stop, int step)
    cdef int random_below  "Storm::random_below"(int number)

cpdef void shuffle(list array):
    for i in reversed(range(len(array) - 1)):
        j = random_range(i, len(array), 1)
        array[i], array[j] = array[j], array[i]


cpdef int randbelow(int a):
    return random_below(a)

cpdef int randint(int a,int b):
    return uniform_int_variate(a, b)

cpdef int randrange(int start,int stop=0,int step=1):
    return random_range(start, stop, step)

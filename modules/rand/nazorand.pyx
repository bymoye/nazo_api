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
    "seed",
    "randbelow", "randint", "randrange",
    "shuffle", 
)

cdef extern from "Rand.hpp":
    void       _seed         "Storm::Engine::cyclone.seed"(unsigned long long)
    long long  _randbelow    "Storm::random_below"(long long)
    long long  _randint      "Storm::uniform_int_variate"(long long, long long)
    long long  _randrange    "Storm::random_range"(long long, long long, long long)

cpdef void seed(int rseed = 0):
    _seed(rseed)

cpdef void shuffle(list array):
    for i in reversed(range(len(array) - 1)):
        j = _randrange(i, len(array), 1)
        array[i], array[j] = array[j], array[i]


cpdef int randbelow(int a):
    return _randbelow(a)

cpdef int randint(int a,int b):
    return _randint(a, b)

cpdef int randrange(int start,int stop=0,int step=1):
    return _randrange(start, stop, step)

# cython: language_level=3
# distutils: language = c++

cpdef void seed(int rseed = ?)
cpdef void shuffle(list array)
cpdef int randbelow(int a)
cpdef int randint(int a,int b)
cpdef int randrange(int start,int stop=?,int step=?)
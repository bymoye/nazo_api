# cython: language_level=3
# distutils: language = c++
from libcpp.vector cimport vector
from libcpp.string cimport string

cdef extern from "yiyan.hpp":
    string      test_cpp     "Hitokoto::getSentence"(vector[char])
    void        init         "Hitokoto::init"(string)

init(b"../../sentences")
cpdef get_test(list v):
    return test_cpp(v)
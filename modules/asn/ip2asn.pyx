# cython: language_level=3
# distutils: language = c++
from libcpp.vector cimport vector
from libcpp.string cimport string

cdef extern from "ipasn.hpp":
    void _init "Address::init"(string ipv4file,string ipv6file)
    vector[string] _lookup "Address::lookup"(string ip) except +


cdef class IpToAsn:
    def __cinit__(self,str ipv4file,str ipv6file):
        _init(ipv4file.encode('UTF-8'),ipv6file.encode('UTF-8'))
    
    def lookup(self,string ip):
        try:
            return _lookup(ip)
        except IndexError:
            return "保留地址"
        except RuntimeError as e:
            return f"错误: {e}" 
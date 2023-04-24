# cython: language_level=3
# distutils: language = c++
from libcpp.vector cimport vector
from libcpp.string cimport string
from libcpp.pair cimport pair
cdef extern from "ipasn.hpp" namespace "Address":
    ctypedef pair[string, string] DataPair
    void init(const string &ipv4file, const string &ipv6file)
    DataPair lookup(const string &ip)

cdef class IpToAsn:
    def __cinit__(self,str ipv4file,str ipv6file):
        init(ipv4file.encode('UTF-8'),ipv6file.encode('UTF-8'))
    
    cpdef tuple lookup(self,string ip):
        cdef DataPair result
        try:
            result = lookup(ip)
        except IndexError:
            return (None,"保留地址")
        except RuntimeError as e:
            return (None,f"错误: {e}" )
        
        return (result.first, result.second)
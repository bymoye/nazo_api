# cython: language_level=3
# distutils: language = c++
from libc.string cimport strstr,strlen,memset
from libc.stdlib cimport atoi,rand,srand
from libcpp.map cimport map
from cython.operator cimport dereference, preincrement
#include './nazorand.pyx'
from .nazorand cimport randbelow
cimport cython
import sys
cdef class Randimg:
    cdef int imgpc_total,imgmb_total
    cdef list imgpc
    cdef list imgmb
    cdef map[char*, int] version_list_c
    cdef bint check_Version(self,char* ua) nogil:
        cdef map[char*,int].iterator end = self.version_list_c.end()
        cdef map[char*,int].iterator it = self.version_list_c.begin()
        cdef char* key
        cdef int value
        cdef char[5] ua_version
        cdef int i1 = 0
        cdef int index
        memset(ua_version,0,5)
        print(ua_version)
        while it != end:
            key = dereference(it).first
            value = dereference(it).second
            index = self.strindex(ua, dereference(it).first)
            if index == -1:
                preincrement(it)
                continue
            i1 = index+strlen(key) + 1
            while b'0' <= ua[i1] <= b'9':
                ua_version[strlen(ua_version)] = ua[i1]
                i1 += 1
            if atoi(ua_version) >= value:
                return True
            memset(ua_version,0,5);
            preincrement(it)

    cdef int strindex(self,char* a,char* b) nogil:
        cdef int n = 0
        cdef int len = strlen(a)
        cdef int result = -1
        if len > 0:
            result = strstr(a, b) - a
        if 0 <= result <= len:
            return result
        return -1

    cdef str pc(self):
        return self.imgpc[randbelow(self.imgpc_total)]
    cdef str moblie(self):
        return self.imgmb[randbelow(self.imgmb_total)]

    cdef list morePc(self,int n,str imgFormat):
        cdef int i
        cdef list r = [self.imgpc[randbelow(self.imgpc_total)] + imgFormat for i in range(n)]
        return r

    cdef list moreMoblie(self,int n,str imgFormat):
        cdef int i
        cdef list r = [self.imgmb[randbelow(self.imgmb_total)] + imgFormat for i in range(n)]
        return r
    
    def process(self,ua:bytes,encode:str|bool,n:int,method:str,form:str) -> str|list:
        cdef str imgFormat
        imgFormat = '!q80.' + (form if form else ('webp' if self.check_Version(ua) else 'jpeg'))
        if encode is None:
            if method == 'moblie':
                return self.Moblie() + imgFormat
            return self.pc() + imgFormat
        if method == 'moblie':
            return self.moreMoblie(n,imgFormat)
        return self.morePc(n,imgFormat)
    
    def __cinit__(self):
        with open("./src/img_url_pc.txt") as pc:
            self.imgpc = pc.read().split()
            self.imgpc_total = len(self.imgpc)
        with open("./src/img_url_mb.txt") as mb:
            self.imgmb = mb.read().split()
            self.imgmb_total = len(self.imgmb)
        version_list = {b'Firefox':65,
                            b'Chrome':32,
                            b'Edge':18,
                            b'AppleWebKit':605, # Safari 14
                            b'OPR':19,
                            b'UCBrowser':12,
                            b'SamsungBrowser':4,
                            b'QQBrowser':10,
                        }
        self.version_list_c = version_list
        version_list = None
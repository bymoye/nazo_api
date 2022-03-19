# cython: language_level=3
# distutils: language = c++
from libc.string cimport strstr,strlen,memset
from libc.stdlib cimport atoi,rand,srand
from libcpp.unordered_map cimport unordered_map
from cython.operator cimport dereference, preincrement
#include './nazorand.pyx'
from .nazorand cimport randbelow
cimport cython
cdef class Randimg:
    cdef int imgpc_total,imgmb_total
    cdef list imgpc
    cdef list imgmb
    cdef unordered_map[char*, int] version_list_c
    cdef bint check_Version(self,char* ua) nogil:
        cdef unordered_map[char*,int].iterator end = self.version_list_c.end()
        cdef unordered_map[char*,int].iterator it = self.version_list_c.begin()
        cdef char* key
        cdef int value
        cdef char[5] uaVersion
        cdef int uaVersionIndex = 0
        cdef int uaIndex
        memset(uaVersion,0,5)
        while it != end:
            derefe = dereference(it)
            key = derefe.first
            value = derefe.second
            uaIndex = self.strindex(ua, key)
            if uaIndex == -1:
                # 如果不存在该UA就跳转到下一个
                preincrement(it)
                continue
            uaVersionIndex = uaIndex + strlen(key) + 1
            while b'0' <= ua[uaVersionIndex] <= b'9':
            # while ua[uaVersionIndex].isdigit():
                uaVersion[strlen(uaVersion)] = ua[uaVersionIndex]
                uaVersionIndex += 1
            if atoi(uaVersion) >= value:
                return True
            memset(uaVersion,0,5)
            preincrement(it)

    cdef int strindex(self,char* a,char* b) nogil:
        cdef int n = 0
        cdef int aLen = strlen(a)
        cdef int result = -1
        if aLen > 0:
            result = strstr(a, b) - a
        if 0 <= result <= aLen:
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
    
    def process(self,ua:bytes,encode:str|bool,n:int,method:str) -> str|list:
        cdef str imgFormat
        imgFormat = '!q80.' + ('webp' if self.check_Version(ua) else 'jpeg')
        if encode is None:
            if method == 'moblie':
                return self.Moblie() + imgFormat
            return self.pc() + imgFormat
        if n > 10:
            n = 10
        if n < 1:
            n = 1
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
        for k ,v in version_list.iteritems():
            self.version_list_c[k] = v
        version_list.clear()
        del version_list
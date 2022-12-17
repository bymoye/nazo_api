# cython: language_level=3
# distutils: language = c++
from libc.string cimport strstr,strlen,memset
from libc.stdlib cimport atoi,rand,srand
from libcpp.unordered_map cimport unordered_map
from libcpp.unordered_set cimport unordered_set
from cython.operator cimport dereference, preincrement
from libcpp.vector cimport vector
from libcpp.string cimport string
#include './nazorand.pyx'
from .nazorand cimport randbelow
import json
cimport cython
ctypedef fused str_or_bool:
    str
    bint
ctypedef fused string_or_list:
    string
    list
cdef:
    string URLWEBP = string(b'webp')
    string PREURL = string(b'https://file.nmxc.ltd/')
    string URLJPEG = string(b'jpeg')
    string SOURCE = string(b'.source.')
    string SLASH = string(b'/')

cdef class Randimg:
    cdef:
        int imgpc_total,imgmb_total
        vector[string] imgpc
        vector[string] imgmb
        unordered_map[char*, int] version_list_c

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

    cdef string pc(self):
        return self.imgpc[randbelow(self.imgpc_total)]
    cdef string moblie(self):
        return self.imgmb[randbelow(self.imgmb_total)]

    cdef list morePc(self,int n,string imgFormat):
        cdef int i
        return [(PREURL + imgFormat + SLASH + self.imgpc[randbelow(self.imgpc_total)] + SOURCE + imgFormat).decode('UTF-8') for i in range(n)]

    cdef list moreMoblie(self,int n,string imgFormat):
        cdef int i
        return [(PREURL + imgFormat + SLASH + self.imgmb[randbelow(self.imgmb_total)] + SOURCE + imgFormat).decode('UTF-8') for i in range(n)]
    
    cpdef process(self,bytes ua,encode,int n,str method):
    #def process(self,ua:bytes,encode:str|bool,n:int,method:str) -> str|list:
        cdef string imgFormat
        imgFormat = URLWEBP if self.check_Version(ua) else URLJPEG
        if encode is None:
            if method == 'mobile':
                return PREURL + imgFormat + SLASH + self.moblie() + SOURCE + imgFormat
            return PREURL + imgFormat + SLASH + self.pc() + SOURCE + imgFormat
        if n > 10:
            n = 10
        if n < 1:
            n = 1
        if method == 'mobile':
         return self.moreMoblie(n,imgFormat)
        return self.morePc(n,imgFormat)
    
    def __cinit__(self):
        with open("./src/manifest.json") as pc:
            temp = json.load(pc)
            for i in temp.keys():
                self.imgpc.push_back(i.encode('UTF-8'))
            self.imgpc_total = self.imgpc.size()
        with open("./src/manifest_mobile.json") as mb:
            temp = json.load(mb)
            for i in temp.keys():
                self.imgmb.push_back(i.encode('UTF-8'))
            self.imgmb_total = self.imgmb.size()

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
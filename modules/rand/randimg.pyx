import json
from libcpp.vector cimport vector
from libcpp.string cimport string
from webp_support.webp_support cimport webp_supported
from nazo_rand.nazo_rand cimport randbelow
from libc.string cimport strcmp

cdef:
    const char* URLWEBP = b'webp'
    const char* PREURL = b'https://file.nmxc.ltd/'
    const char* URLJPEG = b'jpeg'
    const char* SOURCE = b'.source.'
    const char* SLASH = b'/'

cdef class Randimg:
    cdef:
        int imgpc_total, imgmb_total
        vector[string] imgpc, imgmb

    cdef inline string pc(self):
        return self.imgpc[randbelow(self.imgpc_total)]

    cdef inline string moblie(self):
        return self.imgmb[randbelow(self.imgmb_total)]

    cdef list generate_img_urls(self, int n, const char* imgFormat, const char* method):
        cdef int i
        urls = [None] * n
        for i in range(n):
            urls[i] = (PREURL + imgFormat + SLASH + (self.moblie() if strcmp(method, b'mobile') == 0 else self.pc()) + SOURCE + imgFormat).decode('UTF-8')
        return urls

    cpdef str process(self, bytes ua, int n, bytes method):
        cdef const char* imgFormat
        imgFormat = URLWEBP if webp_supported(ua) else URLJPEG

        n = min(max(n, 1), 10)
        urls = self.generate_img_urls(n, imgFormat, method)
        return ' '.join(urls)

    def __cinit__(self):
        cdef str key
        with open("./src/manifest.json") as pc:
            temp = json.load(pc)
            for key in temp.keys():
                self.imgpc.push_back(key.encode('UTF-8'))
            self.imgpc_total = self.imgpc.size()

        with open("./src/manifest_mobile.json") as mb:
            temp = json.load(mb)
            for key in temp.keys():
                self.imgmb.push_back(key.encode('UTF-8'))
            self.imgmb_total = self.imgmb.size()

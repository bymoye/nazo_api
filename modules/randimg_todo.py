import re,fastrand
class randimg:
    def __init__(self) -> None:
        with (open("./src/img_url_pc.txt") as pc,
              open("./src/img_url_mb.txt") as mb):
            self.imgpc = pc.read().split()
            self.imgmb = mb.read().split()
        self.version_list = {'Firefox':65,
                             'Chrome':32,
                             'Edge':18,
                             'AppleWebKit':605,
                             'OPR':19, # Safari 14
                             'UCBrowser':12,
                             'SamsungBrowser':4,
                             'QQBrowser':10,
                            }
        self.imgpc_total = len(self.imgpc)
        self.imgmb_total = len(self.imgmb)
    
    def check_Version(self,ua:list) -> bool:
        e = re.findall(r'(Firefox|Chrome|Edge|AppleWebKit|OPR|UCBrowser|SamsungBrowser|QQBrowser)\/(\d+)', ua)
        for i,j in e:
            if self.version_list[i] < int(j):
                return True
        return False
    
    def pc(self) -> str:
        return self.imgpc[fastrand.pcg32bounded(len(self.imgpc))]
    
    def mb(self) -> str:
        return self.imgmb[fastrand.pcg32bounded(len(self.imgmb))]
    
    def more_pc(self,n,format) -> list:
        return ["".join([self.imgpc[i],format]) for i in [fastrand.pcg32bounded(self.imgpc_total) for _ in range(n)]]
    
    def more_mb(self,n,format) -> list:
        return ["".join([self.imgmb[i],format]) for i in [fastrand.pcg32bounded(self.imgmb_total) for _ in range(n)]]
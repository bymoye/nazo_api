import geoip2.database
from dataclass import Ip_result,Ip_info
from blacksheep.client import ClientSession
import ip2asn
import ipaddress
from modules.sql_todo import sqlite
class _ip:
    def __init__(self, client:ClientSession, key:str,sql:sqlite) -> None:
        self.reader_City = geoip2.database.Reader("./src/GeoLite2-City.mmdb")
        self.reader_ASN_v4 = ip2asn.IP2ASN("./src/ip2asn-v4-u32.tsv")
        self.reader_ASN_v6 = ip2asn.IP2ASN("./src/ip2asn-v6.tsv",ipversion=6)
        self.client,self.sqlite,self.key = client,sql,key
        self.flag={}
    
    def Error(self,msg:str,ip:str|None,clear: bool = False) -> None:
        if clear:
            self.flag.pop(ip)
        raise Exception(msg)
    
        
    async def GetIp(self,ip:str) -> Ip_result:
        try:
            ip_type = ipaddress.ip_address(ip).version
        except:
            raise Exception('IP地址不合法')
        asn = self.reader_ASN_v4.lookup_address_row(ip) if ip_type == 4 else self.reader_ASN_v6.lookup_address_row(ip)
        code = 0
        try:
            City = self.reader_City.city(ip)
            ipinfo = Ip_info(
                            City.country.names['zh-CN'],
                            City.subdivisions.most_specific.name,
                            City.city.name,
                            asn[2] if asn is not None else 0,
                            asn[-1] if asn is not None else ''
                        )
        except:
            ipinfo = self.sqlite.Query_Ip_Table(ip)
            if ipinfo is False:
                if self.flag.get(ip) is None:
                    self.flag[ip] = 1
                else:
                    raise Exception('当前IP正在获取,请勿重复请求')
                req = await self.client.get(f"https://restapi.amap.com/v5/ip?type={ip_type}&ip={ip}&key={self.key}")
                if req is None:
                    self.Error('请求错误',ip,True)
                res = await req.json()
                if res['status'] != '1':
                    self.Error('接口错误,请检查key',ip,True)
                ipinfo = Ip_info(
                                res['country'],
                                res['province'],
                                res['city'],
                                asn[2] if asn is not None else 0,
                                asn[-1] if asn is not None else ''
                            )
                self.sqlite.Write_Ip_Table(ip,ipinfo)
                self.flag.pop(ip)
        return Ip_result(ip,ipinfo,code)
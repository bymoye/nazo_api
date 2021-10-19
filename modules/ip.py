import geoip2.database
import IP2Location
import ip2asn
reader_City = geoip2.database.Reader("./src/GeoLite2-City.mmdb")
reader_ASN = geoip2.database.Reader("./src/GeoLite2-ASN.mmdb")
reader_ip2 = IP2Location.IP2Location("./src/IP2LOCATION-LITE-DB11.BIN")
reader_ASN2 = ip2asn.IP2ASN("./src/ip2asn-v4-u32.tsv")
class ipp:
    def get_ipinfo(self,ip:str = None):
        code = 0
        try:
            City = reader_City.city(ip)
            GEOASN = reader_ASN.asn(ip)
            ipinfo = {"country":City.country.names['zh-CN'],"region":City.subdivisions.most_specific.names['en'],"city":City.city.name,"isp":GEOASN.autonomous_system_organization}
        except:
            try:
                _ipinfo = reader_ip2.get_all(ip)
                asn = reader_ASN2.lookup_address(ip)
                if _ipinfo.country_short == "CN":
                    co = "中国"
                elif _ipinfo.country_short == "-":
                    co = _ipinfo.region = _ipinfo.city = asn['owner'] = "保留地址"
                    code = 2
                else:
                    co = _ipinfo.country_short
                ipinfo = {"country" : co , "region":_ipinfo.region,"city":_ipinfo.city,"isp":asn['owner']}
            except:
                ipinfo = "查询失败"
                code = 1
        return {"data":ipinfo,"code":code}
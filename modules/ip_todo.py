from geoip2.database import Reader
from geoip2.errors import AddressNotFoundError
from maxminddb import MODE_MMAP_EXT
from dataclass import IpResult, IPDataClass
from modules.asn.ip2asn import IpToAsn
from ipaddress import ip_address
import os


class IpUtils:
    def __init__(self) -> None:
        if not os.path.exists("./src/GeoLite2-City.mmdb"):
            raise FileNotFoundError("GeoLite2-City.mmdb文件不存在")
        if not os.path.exists("./src/ip2asn-v4.tsv"):
            raise FileNotFoundError("ip2asn-v4.tsv文件不存在")
        if not os.path.exists("./src/ip2asn-v6.tsv"):
            raise FileNotFoundError("ip2asn-v6.tsv文件不存在")

        self.reader_city = Reader(
            "./src/GeoLite2-City.mmdb", locales=["zh-CN", "en"], mode=MODE_MMAP_EXT
        )
        self.reader_asn = IpToAsn("./src/ip2asn-v4.tsv", "./src/ip2asn-v6.tsv")

    async def get_ip(self, ip: bytes) -> IpResult:
        try:
            _ip = ip_address(ip.decode("utf8"))
            city = self.reader_city.city(_ip)
        except ValueError:
            raise ValueError("IP地址不合法")
        except AddressNotFoundError:
            if _ip.is_private:
                raise ValueError("IP地址为私有地址")
            if _ip.is_multicast:
                raise ValueError("IP地址为组播地址")
            if _ip.is_unspecified:
                raise ValueError("IP地址为未指定地址")

        asn = self.reader_asn.lookup(ip)
        asn_type = type(asn)
        ipinfo = IPDataClass(
            country=city.country.name,
            region=city.subdivisions.most_specific.name,
            city=city.city.name,
            AS=asn if asn_type is str else asn[0].decode(),
            isp=asn if asn_type is str else asn[-1].decode(),
        )
        return IpResult(str(_ip), ipinfo, 0)

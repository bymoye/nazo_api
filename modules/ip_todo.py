import geoip2.database
from maxminddb import MODE_MMAP_EXT
from dataclass import IpResult, IPDataClass
from modules.asn.ip2asn import IpToAsn
import ipaddress


class IpUtils:
    def __init__(self) -> None:
        self.reader_City = geoip2.database.Reader(
            "./src/GeoLite2-City.mmdb", locales=["zh-CN", "en"], mode=MODE_MMAP_EXT
        )
        self.reader_ASN = IpToAsn("./src/ip2asn-v4.tsv", "./src/ip2asn-v6.tsv")

    async def get_ip(self, ip: bytes) -> IpResult:
        try:
            _ip = ipaddress.ip_address(ip.decode("utf8"))
            city = self.reader_City.city(_ip)
        except ValueError:
            raise ValueError("IP地址不合法") from None
        except geoip2.errors.AddressNotFoundError:
            if _ip.is_private:
                raise ValueError("IP地址为私有地址") from None
            if _ip.is_multicast:
                raise ValueError("IP地址为组播地址") from None
            if _ip.is_unspecified:
                raise ValueError("IP地址为未指定地址") from None

        asn = self.reader_ASN.lookup(ip)
        asn_type = type(asn)
        ipinfo = IPDataClass(
            country=city.country.name,
            region=city.subdivisions.most_specific.name,
            city=city.city.name,
            AS=asn if asn_type is str else asn[0].decode(),
            isp=asn if asn_type is str else asn[-1].decode(),
        )
        return IpResult(str(_ip), ipinfo, 0)

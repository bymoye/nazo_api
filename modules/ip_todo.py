import geoip2.database
from maxminddb import MODE_MMAP_EXT
from dataclass import Ip_result, Ip_info
from blacksheep.client import ClientSession
from modules.asn.ip2asn import IpToAsn
import ipaddress
from modules.sql_todo import SelfSqlite


class IpCheck:
    def __init__(self, client: ClientSession, key: str, sql: SelfSqlite) -> None:
        self.reader_City = geoip2.database.Reader(
            "./src/GeoLite2-City.mmdb", locales=["zh-CN", "en"], mode=MODE_MMAP_EXT
        )
        self.reader_ASN = IpToAsn("./src/ip2asn-v4.tsv", "./src/ip2asn-v6.tsv")
        self.client, self.sqlite, self.key = client, sql, key
        self.flag = {}

    def Error(self, msg: str, ip: str | None, clear: bool = False) -> None:
        if clear:
            self.flag.pop(ip)
        raise Exception(msg)

    async def get_ip(self, ip: bytes) -> Ip_result:
        try:
            _ip = ipaddress.ip_address(ip.decode("utf8"))
            city = self.reader_City.city(_ip)
        except ValueError:
            # return Ip_result(ip=ip,country=None,city=None,asn=None)
            raise ValueError("IP地址不合法") from None
        except geoip2.errors.AddressNotFoundError:
            if _ip.is_private:
                raise ValueError("IP地址为私有地址") from None
            if _ip.is_multicast:
                raise ValueError("IP地址为组播地址") from None
            if _ip.is_unspecified:
                raise ValueError("IP地址为未指定地址") from None

        asn = self.reader_ASN.lookup(ip)
        ipinfo = Ip_info(
            country=city.country.name,
            region=city.subdivisions.most_specific.name,
            city=city.city.name,
            AS=asn[0].decode() if type(asn) is not str else asn,
            isp=asn[-1].decode() if type(asn) is not str else asn,
        )
        return Ip_result(str(_ip), ipinfo, 0)

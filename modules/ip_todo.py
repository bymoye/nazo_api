from geoip2.database import Reader
from maxminddb import MODE_MMAP_EXT
from dataclass import IpResult, IPDataClass
from nazo_ip2asn import Ip2Asn
from pathlib import Path
from ipaddress import ip_address
from typing import Optional, Union


class IpUtils:
    def __init__(
        self,
        geolite2_city_path: Union[str, Path],
        ip2asn_v4_path: Union[str, Path],
        ip2asn_v6_path: Union[str, Path],
    ) -> None:
        if isinstance(geolite2_city_path, str):
            geolite2_city_path = Path(geolite2_city_path)
        if isinstance(ip2asn_v4_path, str):
            ip2asn_v4_path = Path(ip2asn_v4_path)
        if isinstance(ip2asn_v6_path, str):
            ip2asn_v6_path = Path(ip2asn_v6_path)
        # if not os.path.exists("./src/GeoLite2-City.mmdb"):
        if not geolite2_city_path.exists():
            raise FileNotFoundError("GeoLite2-City.mmdb文件不存在")
        # if not os.path.exists("./src/ip2asn-v4.tsv"):
        if not ip2asn_v4_path.exists():
            raise FileNotFoundError("ip2asn-v4.tsv文件不存在")
        # if not os.path.exists("./src/ip2asn-v6.tsv"):
        if not ip2asn_v6_path.exists():
            raise FileNotFoundError("ip2asn-v6.tsv文件不存在")

        self.reader_city = Reader(
            geolite2_city_path, locales=["zh-CN", "en"], mode=MODE_MMAP_EXT
        )
        self.reader_asn = Ip2Asn(str(ip2asn_v4_path), str(ip2asn_v6_path))

    def get_ip(self, ip: bytes) -> IpResult:
        try:
            _ip = ip_address(ip.decode("utf8"))
        except ValueError:
            raise ValueError("IP地址不合法")
        if _ip.is_private:
            raise ValueError("IP地址为私有地址")
        if _ip.is_multicast:
            raise ValueError("IP地址为组播地址")
        if _ip.is_unspecified:
            raise ValueError("IP地址为未指定地址")
        city = self.reader_city.city(_ip)

        _as, isp = self.reader_asn.lookup(ip)
        if isinstance(_as, bytes):
            _as = _as.decode()
        if isinstance(isp, bytes):
            isp = isp.decode()

        ipinfo = IPDataClass(
            country=city.country.name,
            region=city.subdivisions.most_specific.name,
            city=city.city.name,
            AS=_as,
            isp=isp,
        )
        return IpResult(str(_ip), ipinfo, 0)

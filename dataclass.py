from dataclasses import dataclass
from abc import ABC


@dataclass
class IPDataClass:
    country: str
    region: str
    city: str
    AS: int
    isp: str


@dataclass
class QQDataClass:
    qqnumber: int
    qqname: str
    qqavatar: str


@dataclass
class IpResult:
    ip: str = None
    data: IPDataClass = None
    code: int = None


@dataclass
class UADataClass:
    ip: str
    header: dict
    ipinfo: IPDataClass


@dataclass
class RandImgDataClass:
    code: int
    url: str

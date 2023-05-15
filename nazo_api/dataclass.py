from dataclasses import dataclass
from abc import ABC
from typing import Optional, Union


@dataclass
class IPDataClass:
    country: Optional[str]
    region: Optional[str]
    city: Optional[str]
    AS: Optional[str]
    isp: Optional[str]


@dataclass
class QQDataClass:
    qq_number: str
    qq_name: str
    qq_avatar: str


@dataclass
class IpResult:
    ip: Optional[str] = None
    data: Optional[IPDataClass] = None
    code: Optional[int] = None


@dataclass
class UADataClass:
    ip: str
    header: dict
    ipinfo: Optional[IPDataClass]


@dataclass
class RandImgDataClass:
    code: int
    url: list

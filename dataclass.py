from dataclasses import dataclass
from abc import ABC
@dataclass
class Ip_info:
    country: str
    region: str
    city: str
    AS: int
    isp: str

@dataclass
class Qq_info:
    qqnumber: int
    qqname: str
    qqavatar: str

@dataclass
class Ip_result:
    ip : str = None
    data: Ip_info|str = None
    code: int = None

@dataclass
class Get_ua_result:
    ip : str
    header : dict
    ipinfo : Ip_info

@dataclass
class randimg_result:
    code : int
    url : str|list

class sql(ABC):
    pass

class httpclient(ABC):
    pass

class config(ABC):
    pass

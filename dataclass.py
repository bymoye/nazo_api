from dataclasses import dataclass
from dataclasses_json import dataclass_json
from abc import ABC
@dataclass_json
@dataclass
class Ip_info:
    country: str
    province: str
    city: str
    AS: int
    isp: str

@dataclass_json
@dataclass
class Qq_info:
    qqnumber: int
    qqname: str
    qqavatar: str

@dataclass
class Ip_result:
    ip : str
    data: Ip_info|str
    code: int

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


from dataclasses import dataclass
import yaml

@dataclass
class Global:
    port: int = 8000

@dataclass
class ty:
    enable: bool = False

@dataclass
class ip(ty):
    key: str = None
    
@dataclass
class Module:
    qq: ty
    yiyan: ty
    ip: ip
    randimg: ty
    ua: ty
    

@dataclass
class _ApiConfig:
    _global: Global
    module: Module


class ApiConfig:
    def __init__(self) -> None:
        with open('config.yaml', mode='r',encoding="UTF-8") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        self.config:dict = _ApiConfig(**config)

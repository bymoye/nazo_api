from dataclasses import dataclass
import yaml


@dataclass
class Global:
    port: int = 8000


@dataclass
class Option:
    enable: bool = False


@dataclass
class Module:
    qq: Option
    yiyan: Option
    ip: Option
    randimg: Option
    ua: Option


@dataclass
class _ApiConfig:
    god: Global
    module: Module


class ApiConfig:
    def __init__(self) -> None:
        with open("config.yaml", mode="r", encoding="UTF-8") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)

        self.config = _ApiConfig(
            god=Global(**config["_global"]),
            module=Module(
                qq=Option(**config["module"]["qq"]),
                yiyan=Option(**config["module"]["yiyan"]),
                ip=Option(**config["module"]["ip"]),
                randimg=Option(**config["module"]["randimg"]),
                ua=Option(**config["module"]["ua"]),
            ),
        )

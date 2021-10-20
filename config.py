from typing import Any
from parse_it import ParseIt

class ApiConfig:
    def __init__(self) -> None:
        self.parser = ParseIt(config_type_priority=['env'])
        self.port: int = self.get_Config('port', 8000, [int])
        self.ip_key: str = self.get_Config('ip_key', 'test', [str])

    def get_Config(self,name: str, default, allowed: list = None):
        return self.parser.read_configuration_variable(name, default_value=default, allowed_types=allowed)

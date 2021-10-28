from rodi import Container
from config import ApiConfig
from dataclass import config
service = Container()
service.add_instance(ApiConfig(),declared_class=config)
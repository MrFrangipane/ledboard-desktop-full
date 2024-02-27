from dataclasses import dataclass

from ledboarddesktopfull.core.configuration import Configuration
from ledboarddesktopfull.python_extensions.singleton_metaclass import SingletonMetaclass
from ledboardclientfull import LEDBoardClientAPI


@dataclass
class Components(metaclass=SingletonMetaclass):
    configuration = Configuration()
    board_api = LEDBoardClientAPI()

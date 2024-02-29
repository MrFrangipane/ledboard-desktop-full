from dataclasses import dataclass

from ledboardclientfull import LEDBoardClientAPI

from ledboarddesktopfull.components.scan.image_processing.image_processor import ScanImageProcessor
from ledboarddesktopfull.core.configuration import Configuration
from ledboarddesktopfull.python_extensions.singleton_metaclass import SingletonMetaclass


@dataclass
class Components(metaclass=SingletonMetaclass):
    configuration = Configuration()
    board_api = LEDBoardClientAPI()
    scan_image_processor = ScanImageProcessor()

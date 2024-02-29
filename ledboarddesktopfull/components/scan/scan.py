from ledboarddesktopfull.components.scan.image_processing.image_processor import ScanImageProcessor
from ledboarddesktopfull.components.scan.viewport.widget import ScanViewport


class Scan:
    def __init__(self):
        self.image_processor = ScanImageProcessor()
        self.viewport = ScanViewport()

    def save(self):
        pass

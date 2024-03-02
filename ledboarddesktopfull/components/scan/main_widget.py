from PySide6.QtWidgets import QWidget, QHBoxLayout

from pyside6helpers.group import make_group

from ledboarddesktopfull.components.scan.viewport.widget import ScanViewport
from ledboarddesktopfull.components.scan.options import ScanOptions


class ScanMainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Widgets
        self.options = ScanOptions()
        self.viewport = ScanViewport()

        #
        # Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(make_group("Viewport", [self.viewport]), 100)
        layout.addWidget(self.options)

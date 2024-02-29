from PySide6.QtWidgets import QWidget, QGridLayout

from pyside6helpers.group import make_group

from ledboarddesktopfull.components.scan.viewport_interactors.navigator import Navigator
from ledboarddesktopfull.components.scan.viewport_interactors.polygon_drawer import PolygonDrawer
from ledboarddesktopfull.components.scan.widgets.options import ScanOptions
from ledboarddesktopfull.components.scan.widgets.viewport import ScanViewport
from ledboarddesktopfull.components.scan.widgets.tools import ScanTools


class ScanMainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Widgets
        self.options = ScanOptions()
        self.tools = ScanTools()
        self.viewport = ScanViewport()

        #
        # FIXME hacky
        self.viewport_navigator = Navigator(self.viewport.view)
        self.viewport_polygon_drawer = PolygonDrawer(self.viewport.view)

        self.viewport.view.interactors.append(self.viewport_navigator)
        self.viewport.view.interactors.append(self.viewport_polygon_drawer)

        #
        # Layout
        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(make_group("Tools", [self.tools]))
        layout.addWidget(make_group("Viewport", [self.viewport]), 0, 1)
        layout.addWidget(self.options, 0, 2)

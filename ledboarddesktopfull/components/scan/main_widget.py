from PySide6.QtWidgets import QWidget, QHBoxLayout

from pyside6helpers.group import make_group

from ledboarddesktopfull.components.scan.viewport.widget import ScanViewport
from ledboarddesktopfull.components.scan.settings import ScanSettingsWidget


class ScanMainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Widgets
        self.settings = ScanSettingsWidget()
        self.viewport = ScanViewport()

        #
        # Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(make_group("Viewport", [self.viewport]), 100)
        layout.addWidget(self.settings)

    # FIXME flatten this in UiComponents
    def load_from_client(self):
        self.settings.load_from_client()
        self.viewport.load_from_client()

    # FIXME flatten this in UiComponents
    def clear_detection_points(self):
        self.viewport.clear_detection_points()

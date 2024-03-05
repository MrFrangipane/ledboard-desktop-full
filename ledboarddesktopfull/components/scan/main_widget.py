from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QHBoxLayout

from pyside6helpers.group import make_group

from ledboarddesktopfull.components.scan.viewport.widget import ScanViewport
from ledboarddesktopfull.components.scan.side_bar import ScanSideBar


class ScanMainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Widgets
        self.side_bar = ScanSideBar()
        self.viewport = ScanViewport()

        #
        # Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(make_group("Viewport", [self.viewport]), 100)
        layout.addWidget(self.side_bar)

        # FIXME flatten this in UiComponents
        # FIXME choose between refresh and update and stick to it
        self.viewport.viewportUpdated.connect(self.side_bar.refresh_detection_infos)

    # FIXME flatten this in UiComponents
    def load_from_client(self):
        self.side_bar.load_from_client()
        self.viewport.load_from_client()

    # FIXME flatten this in UiComponents
    def clear_detection_points(self):
        self.viewport.clear_detection_points()

    # FIXME flatten this in UiComponents
    def start_viewport_update_timer(self):
        self.viewport.start_viewport_update_timer()

    # FIXME flatten this in UiComponents
    def stop_viewport_update_timer(self):
        self.viewport.stop_viewport_update_timer()
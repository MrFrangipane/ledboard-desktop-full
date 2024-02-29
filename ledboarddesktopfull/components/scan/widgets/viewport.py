from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QGridLayout, QGraphicsScene

from ledboarddesktopfull.core.components import Components
from ledboarddesktopfull.python_extensions.graphics_view import GraphicsView


class ScanViewport(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.scene = QGraphicsScene()
        self.image_plane = self.scene.addPixmap(QPixmap())

        self.view = GraphicsView()
        self.view.setScene(self.scene)

        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.view)

        self._viewport_timer = QTimer(self)
        self._viewport_timer.timeout.connect(self._update_viewport)
        self._viewport_timer.start(int(1000 / Components().configuration.scan_viewport_framerate))

    def _update_viewport(self):
        self.image_plane.setPixmap(Components().scan_image_processor.viewport_pixmap())

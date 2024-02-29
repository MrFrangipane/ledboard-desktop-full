from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QHBoxLayout, QGraphicsScene

from ledboarddesktopfull.components.scan.viewport.interactors.navigator import Navigator
from ledboarddesktopfull.components.scan.viewport.interactors.mask_drawer import MaskDrawer
from ledboarddesktopfull.components.scan.viewport.tools import ScanViewportTools
from ledboarddesktopfull.core.components import Components
from ledboarddesktopfull.python_extensions.graphics_view import GraphicsView


class ScanViewport(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        #
        # Widgets
        self.scene = QGraphicsScene()
        self.image_plane = self.scene.addPixmap(QPixmap())

        self.view = GraphicsView()
        self.view.setScene(self.scene)

        self.tools = ScanViewportTools()

        #
        # Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.tools)
        layout.addWidget(self.view, 100)

        self._viewport_timer = QTimer(self)
        self._viewport_timer.timeout.connect(self._update_viewport)
        self._viewport_timer.start(int(1000 / Components().configuration.scan_viewport_framerate))

        #
        # Interactors
        self.viewport_navigator = Navigator(self.view)
        self.viewport_mask_drawer = MaskDrawer(self.view)

        self.view.interactors.append(self.viewport_navigator)
        self.view.interactors.append(self.viewport_mask_drawer)

        #
        # Signals
        self.tools.maskEditingChanged.connect(self._mask_editing_changed)
        self.tools.maskResetClicked.connect(self._mask_reset)

    def _update_viewport(self):
        self.image_plane.setPixmap(Components().scan_image_processor.viewport_pixmap())

    def _mask_editing_changed(self, is_active):
        self.viewport_mask_drawer.is_active = is_active

    def _mask_reset(self):
        self.viewport_mask_drawer.reset()

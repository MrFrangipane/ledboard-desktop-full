from typing import Callable

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QGraphicsPixmapItem


class GraphicsImagePlane(QGraphicsPixmapItem):
    pixmapSizeChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._on_size_change_callback: Callable = None
        self._previous_size = self.pixmap().size()

    def set_on_size_change_callback(self, callback: Callable):
        self._on_size_change_callback = callback

    def setPixmap(self, pixmap):
        QGraphicsPixmapItem.setPixmap(self, pixmap)

        if pixmap.size() != self._previous_size:
            self._previous_size = pixmap.size()
            self._on_size_change_callback()

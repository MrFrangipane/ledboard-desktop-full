from PySide6.QtCore import Qt
from PySide6.QtGui import QPolygon, QPen, QBrush, QColor

from ledboarddesktopfull.python_extensions.abstract_graphicsview_interactor import AbstractGraphicsViewInteractor


class PolygonDrawer(AbstractGraphicsViewInteractor):
    def __init__(self, view):
        super().__init__(view)
        self.is_enabled = True

        self._is_active = False
        self._is_drawing = False

        pen = QPen(QColor(255, 0, 128))
        pen.setWidth(2)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)

        brush = QBrush(QColor(255, 0, 128, 64))

        self._polygon = QPolygon()
        self._polygon_item = self._view.scene().addPolygon(self._polygon, pen, brush)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control:
            self._is_active = False

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self._is_active = True

    def mousePressEvent(self, event):
        if not self._is_active:
            return

        position = self._view.mapToScene(event.position().toPoint())
        polygon = self._polygon_item.polygon()
        polygon.append(position)
        self._polygon_item.setPolygon(polygon)

    def mouseMoveEvent(self, event):
        pass

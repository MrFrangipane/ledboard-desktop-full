import numpy as np

from PySide6.QtCore import Qt
from PySide6.QtGui import QPolygonF, QPen, QBrush, QColor

from ledboarddesktopfull.python_extensions.abstract_graphicsview_interactor import AbstractGraphicsViewInteractor


class MaskDrawer(AbstractGraphicsViewInteractor):
    def __init__(self, view):
        super().__init__(view)
        self.is_enabled = True

        self.is_active = False
        self._temp_disable = False
        self._is_drawing = False

        pen = QPen(QColor(255, 0, 128))
        pen.setWidth(2)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)

        brush = QBrush(QColor(255, 0, 128, 64))

        self._polygon = QPolygonF()
        self._polygon_item = self._view.scene().addPolygon(self._polygon, pen, brush)
        self.reset()

    @property
    def mask_item(self):
        return self._polygon_item

    @property
    def mask_geometry(self):  # fixme use a dataclass
        points = np.array([
            [int(self._polygon.at(i).x()), int(self._polygon.at(i).y())]
            for i in range(self._polygon.count())
        ])
        return points

    def reset(self):
        self._polygon = QPolygonF()
        self._polygon_item.setPolygon(self._polygon)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control:
            self._temp_disable = True

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self._temp_disable = False

    def mousePressEvent(self, event):
        if self._temp_disable or not self.is_active:
            return

        position = self._view.mapToScene(event.position().toPoint())
        self._polygon.append(position)
        self._polygon_item.setPolygon(self._polygon)

    def mouseMoveEvent(self, event):
        return
        """
        if self._temp_disable or not self.is_active:
            return

        position = self._view.mapToScene(event.position().toPoint())
        polygon = self._polygon_item.polygon()
        if polygon.isEmpty():
            return

        polygon.last().setX(position.x())
        polygon.last().setY(position.y())
        self._polygon_item.setPolygon(polygon)
        """

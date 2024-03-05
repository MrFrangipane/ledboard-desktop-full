from copy import copy

from PySide6.QtGui import QPen, QColor
from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsItem

from ledboardclientfull import DetectionPoint


class DetectionPointGraphicsItem(QGraphicsEllipseItem):
    IndexedColors = {
        -1: QColor(200, 200, 200),
        0: QColor(255, 0, 0),
        1: QColor(0, 255, 0),
        2: QColor(0, 0, 255),
        3: QColor(0, 255, 255),
        4: QColor(255, 0, 255),
    }

    def __init__(self, detection_point: DetectionPoint, parent=None):
        super().__init__(parent)

        self.detection_point = copy(detection_point)

        self.setRect(-3, -3, 6, 6)
        self.setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable |
            QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
        )

    def paint(self, painter, option, widget=None):
        pen = QPen()
        pen.setWidth(2)
        pen.setColor(self.IndexedColors[self.detection_point.assigned_segment_number])
        self.setPen(pen)
        QGraphicsEllipseItem.paint(self, painter, option, widget)

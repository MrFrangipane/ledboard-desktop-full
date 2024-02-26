from dataclasses import dataclass

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QPainter, QColor, QBrush
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class _HandleGeometry:
    Padding = 5
    HandleWidth = 5


@dataclass
class Handle:
    value: float
    rect: QRectF = QRectF()
    is_hover: bool = False
    is_selected: bool = False


class GradientBarWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)

        self.handles = [
            Handle(value=0.0),
            Handle(value=0.25),
            Handle(value=0.5),
            Handle(value=1.0)
        ]
        self.selected_handle = None

        self._update_handles_rects()

    def _update_handles_rects(self):
        self._handles_rects = list()
        for handle in self.handles:
            handle.rect = QRectF(
                _HandleGeometry.Padding + (self.width() - (2.0 * _HandleGeometry.Padding)) * handle.value - (_HandleGeometry.HandleWidth / 2.0),
                _HandleGeometry.Padding,
                _HandleGeometry.HandleWidth,
                self.height() - (2.0 * _HandleGeometry.Padding)
            )
        self.update()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        for handle in self.handles:
            if handle.is_hover:
                painter.setBrush(QBrush(QColor(255, 0, 0)))
            else:
                painter.setBrush(QBrush(QColor(255, 255, 0)))

            if handle.is_selected:
                painter.setBrush(QBrush(QColor(255, 255, 255)))

            painter.drawRect(handle.rect)

        painter.end()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.selected_handle is not None:
            value = max(0.0, min(1.0, event.pos().x() / self.width()))
            self.selected_handle.value = value

        else:
            for handle in self.handles:
                handle.is_hover = handle.rect.contains(event.pos())

        self._update_handles_rects()

    def mousePressEvent(self, event):
        self.selected_handle = None
        for handle in self.handles:
            handle.is_selected = handle.rect.contains(event.pos())
            if handle.is_selected:
                self.selected_handle = handle

        self.update()

    def resizeEvent(self, event):
        self._update_handles_rects()

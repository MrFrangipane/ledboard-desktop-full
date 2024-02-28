from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QFrame, QGraphicsView

from ledboarddesktopfull.python_extensions.abstract_graphicview_interactor import AbstractGraphicsViewInteractor


class GraphicsView(QGraphicsView):

    def __init__(self, interactors: list[AbstractGraphicsViewInteractor], parent=None):
        QGraphicsView.__init__(self, parent)

        self.setRenderHint(QPainter.Antialiasing, True)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setOptimizationFlag(QGraphicsView.DontAdjustForAntialiasing)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFrameShape(QFrame.Shape.NoFrame)

        self.interactors = interactors

    def keyPressEvent(self, event):
        for interactor in self.interactors:
            if interactor.is_enabled:
                interactor.keyPressEvent(self, event)
        QGraphicsView.keyPressEvent(self, event)

    def keyReleaseEvent(self, event):
        for interactor in self.interactors:
            if interactor.is_enabled:
                interactor.keyReleaseEvent(self, event)
        QGraphicsView.keyReleaseEvent(self, event)

    def wheelEvent(self, event):
        for interactor in self.interactors:
            if interactor.is_enabled:
                interactor.wheelEvent(self, event)
        QGraphicsView.wheelEvent(self, event)

    def mousePressEvent(self, event):
        for interactor in self.interactors:
            if interactor.is_enabled:
                interactor.mousePressEvent(self, event)
        QGraphicsView.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        for interactor in self.interactors:
            if interactor.is_enabled:
                interactor.mouseMoveEvent(self, event)
        QGraphicsView.mouseMoveEvent(self, event)

    def resizeEvent(self, event):
        for interactor in self.interactors:
            if interactor.is_enabled:
                interactor.resizeEvent(self, event)
        QGraphicsView.resizeEvent(self, event)

from PySide6.QtCore import Qt, QRectF

from ledboarddesktopfull.python_extensions.abstract_graphicview_interactor import AbstractGraphicsViewInteractor


class Navigator(AbstractGraphicsViewInteractor):
    def __init__(self):
        super().__init__()
        self.is_enabled = True

        self._zoom = 0
        self._drag_anchor = 0, 0
        self._frustum = QRectF(0, 0, 0, 0)

    def _update_frustum(self, view):
        view.setSceneRect(self._frustum)
        view.fitInView(self._frustum, Qt.KeepAspectRatio)

    def wheelEvent(self, view, event):
        if event.angleDelta().y() > 0:
            factor = 1.25
        else:
            factor = 0.8

        position = view.mapToScene(event.position().toPoint())
        w = self._frustum.width() / factor
        h = self._frustum.height() / factor

        self._frustum = QRectF(
            position.x() - (position.x() - self._frustum.left()) / factor,
            position.y() - (position.y() - self._frustum.top()) / factor,
            w, h
        )
        self._update_frustum(view)

    def mousePressEvent(self, view, event):
        self._drag_anchor = view.mapToScene(event.position().toPoint())

    def mouseMoveEvent(self, view, event):
        position = view.mapToScene(event.position().toPoint())
        delta = self._drag_anchor - position

        self._frustum.adjust(delta.x(), delta.y(), delta.x(), delta.y())
        self._update_frustum(view)

    def resizeEvent(self, view, event):
        self._frustum = QRectF(0, 0, view.size().width(), view.size().height())
        self._update_frustum(view)
        """
        w, h = self.size().width(), self.size().height()
        if 0 in [w, h]:
            self.resize(self._last_size)
        delta = max(w / self._last_size.width(), h / self._last_size.height())
        self._set_viewer_zoom(delta)
        self._last_size = self.size()
        super(NodeViewer, self).resizeEvent(event)
    """

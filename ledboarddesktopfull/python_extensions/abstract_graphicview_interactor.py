

class AbstractGraphicsViewInteractor:

    def __init__(self):
        self.is_enabled = False

    def keyPressEvent(self, view, event):
        pass

    def keyReleaseEvent(self, view, event):
        pass

    def wheelEvent(self, view, event):
        pass

    def mousePressEvent(self, view, event):
        pass

    def mouseMoveEvent(self, view, event):
        pass

    def resizeEvent(self, view, event):
        pass

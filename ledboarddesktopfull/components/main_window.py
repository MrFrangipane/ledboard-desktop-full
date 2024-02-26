import os.path

from PySide6.QtCore import Signal
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QMainWindow, QLabel

from ledboarddesktopfull.core.components import Components
from ledboarddesktopfull.components.gradient.widget.gradient_bar import GradientBarWidget


class MainWindow(QMainWindow):
    shown = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("LED Board")

        icon_filepath = os.path.join(Components().configuration.resources_folder, "application-icon.png")
        self.setWindowIcon(QIcon(icon_filepath))

        logo_filepath = os.path.join(Components().configuration.resources_folder, "frangitron-logo.png")
        logo_pixmap = QPixmap(logo_filepath)
        logo_label = QLabel()
        logo_label.setPixmap(logo_pixmap)
        self.statusBar().addPermanentWidget(logo_label)

        self.central = GradientBarWidget()
        self.setCentralWidget(self.central)

    def showEvent(self, event):
        self.shown.emit()
        event.accept()

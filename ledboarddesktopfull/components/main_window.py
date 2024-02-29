import os.path

from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QLabel, QMainWindow

from ledboarddesktopfull.core.components import Components


class MainWindow(QMainWindow):

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

        # FIXME could be better
        self.timer_callbacks = QTimer()
        self.timer_callbacks.timeout.connect(self.run_callbacks)

    def showEvent(self, event):
        QMainWindow.showEvent(self, event)
        self.timer_callbacks.start(0)

    def run_callbacks(self):
        self.timer_callbacks.stop()
        for callback in Components().configuration.on_main_window_shown_callbacks:
            callback()

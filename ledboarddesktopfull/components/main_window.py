import os.path

from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QLabel, QMainWindow

from ledboarddesktopfull.core.ui_components import UiComponents


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("LED Board")

        icon_filepath = os.path.join(UiComponents().configuration.resources_folder, "application-icon.png")
        self.setWindowIcon(QIcon(icon_filepath))

        logo_filepath = os.path.join(UiComponents().configuration.resources_folder, "frangitron-logo.png")
        logo_pixmap = QPixmap(logo_filepath)
        logo_label = QLabel()
        logo_label.setPixmap(logo_pixmap)
        self.statusBar().addPermanentWidget(logo_label)

        # FIXME could be better
        self._already_shown_once = False
        self.timer_on_shown = QTimer()
        self.timer_on_shown.timeout.connect(self._on_first_shown)

    def showEvent(self, event):
        QMainWindow.showEvent(self, event)
        if not self._already_shown_once:
            self._already_shown_once = True
            self.timer_on_shown.start(0)

    def _on_first_shown(self):
        self.timer_on_shown.stop()
        UiComponents().project_persistence.load_from_working()

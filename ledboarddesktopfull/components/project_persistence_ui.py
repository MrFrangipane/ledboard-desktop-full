import os.path

from PySide6.QtCore import QObject
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenuBar, QFileDialog

from pyside6helpers import icons

from ledboardclientfull import project as project_api

from ledboarddesktopfull.core.components import Components


class ProjectPersistenceUi(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.action_new = QAction(icons.file(), "&New project")
        self.action_new.triggered.connect(project_api.new)

        self.action_load = QAction(icons.folder(), "&Load project...")
        self.action_load.triggered.connect(self.load)

        self.action_save = QAction(icons.diskette(), "&Save project...")
        self.action_save.triggered.connect(self.save)

    def add_actions_to_menu(self, menu_bar: QMenuBar):
        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction(self.action_new)
        file_menu.addAction(self.action_load)
        file_menu.addAction(self.action_save)

    def load(self):
        dialog = QFileDialog()
        filepath, _ = dialog.getOpenFileName()
        if filepath:
            project_api.load(filepath)
            self._update_widgets()

    def save(self):
        dialog = QFileDialog()
        filepath, _ = dialog.getSaveFileName()
        if filepath:
            project_api.save(filepath)

    @staticmethod
    def save_as_working():
        project_api.save(os.path.expanduser("~/ledboard-working-project.json"))

    def load_from_working(self):
        project_api.load(os.path.expanduser("~/ledboard-working-project.json"))
        self._update_widgets()

    def _update_widgets(self):
        # Components().board_selector.set_selected_board(project.board_port_name)
        # FIXME: should we move "post main window show callbacks" to here ?
        pass

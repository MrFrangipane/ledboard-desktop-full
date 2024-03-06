import logging
import os.path

from PySide6.QtCore import QObject
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu, QFileDialog

from pyside6helpers import icons

from ledboardclientfull import project_api ,board_api

from ledboarddesktopfull.core.ui_components import UiComponents

_logger = logging.getLogger(__name__)


class UiProjectPersistence(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.action_save_working = QAction(icons.briefcase(), "Save to &working file")
        self.action_save_working.triggered.connect(self.save_as_working)

        self.action_new = QAction(icons.file(), "&New project")
        self.action_new.triggered.connect(self.new)
        self.action_new.setEnabled(False)

        self.action_load = QAction(icons.folder(), "&Load project...")
        self.action_load.triggered.connect(self.load)

        self.action_save = QAction(icons.diskette(), "&Save project...")
        self.action_save.triggered.connect(self.save)

    def add_actions_to_menu(self, menu: QMenu):
        _logger.info("Adding actions to menu bar")
        menu.addAction(self.action_save_working)
        menu.addSeparator()
        menu.addAction(self.action_new)
        menu.addAction(self.action_load)
        menu.addAction(self.action_save)

    def new(self):
        project_api.new()
        self._update_widgets()

    def load(self):
        dialog = QFileDialog()
        filepath, _ = dialog.getOpenFileName()
        if filepath:
            self._load(filepath)

    def save(self):
        dialog = QFileDialog()
        filepath, _ = dialog.getSaveFileName()
        if filepath:
            self._save(filepath)

    def save_as_working(self):
        _logger.info("Saving project working file")
        self._save(os.path.expanduser("~/ledboard-working-project.json"))

    def load_from_working(self):
        _logger.info("Loading project working file")
        self._load(os.path.expanduser("~/ledboard-working-project.json"))

    def _load(self, filepath):
        UiComponents().widgets.scan.stop_viewport_update_timer()
        board_api.available_boards()  # FIXME hack to prevent semaphore windows
        project_api.load(filepath)
        self._update_widgets()
        UiComponents().widgets.scan.start_viewport_update_timer()

    @staticmethod
    def _save(filepath):
        UiComponents().widgets.scan.stop_viewport_update_timer()
        project_api.save(filepath)
        UiComponents().widgets.scan.start_viewport_update_timer()

    @staticmethod
    def _update_widgets():
        UiComponents().widgets.board_selector.load_from_client()
        UiComponents().widgets.board_configurator.load_from_client()
        UiComponents().widgets.board_illuminator.load_from_client()
        UiComponents().widgets.scan.load_from_client()

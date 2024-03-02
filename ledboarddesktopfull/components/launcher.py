import logging
import os.path

from PySide6.QtCore import QObject
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication

from pyside6helpers import css, icons
from pyside6helpers.logger import dock_logger_to_main_window

from ledboardclientfull import init_ledboard_client

from ledboarddesktopfull.components.board.configurator import BoardConfiguratorWidget
from ledboarddesktopfull.components.board.illuminator import BoardIlluminatorWidget
from ledboarddesktopfull.components.board.selector import BoardSelectorWidget
from ledboarddesktopfull.components.central_widget import CentralWidget
from ledboarddesktopfull.components.main_window import MainWindow
from ledboarddesktopfull.components.scan.main_widget import ScanMainWidget
from ledboarddesktopfull.components.ui_project_persistence import UiProjectPersistence
from ledboarddesktopfull.core.ui_components import UiComponents as UiC

_logger = logging.getLogger(__name__)
_show_css_editor = False
_save_on_quit = True


class Launcher(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        init_ledboard_client()

        UiC().configuration.resources_folder = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "resources"
        )

        self._application = QApplication()
        css.load_onto(self._application)

        self.action_quit = QAction(icons.right_arrow(), "&Quit")
        self.action_quit.triggered.connect(self._application.quit)

        self._main_window = MainWindow()
        dock_logger_to_main_window(self._main_window)
        self._main_window.resize(950, 600)

        # /!\ After MainWindow and before CentralWidget
        self._init_ui_components()

        self._central_widget = CentralWidget()
        self._main_window.setCentralWidget(self._central_widget)

        logging.basicConfig(level=logging.INFO)

        if _show_css_editor:
            from pyside6helpers.css.editor import CSSEditor
            self.css_editor = CSSEditor("Frangitron", QApplication.instance())

        if _save_on_quit:
            self._application.aboutToQuit.connect(UiC().project_persistence.save_as_working)

        self._init_menus()

    def exec(self) -> int:
        self._main_window.showMaximized()
        return self._application.exec()

    def _init_menus(self):
        menu_bar = self._main_window.menuBar()
        file_menu = menu_bar.addMenu("&File")
        UiC().project_persistence.add_actions_to_menu(file_menu)
        file_menu.addSeparator()
        file_menu.addAction(self.action_quit)

    @staticmethod
    def _init_ui_components():
        UiC().widgets.board_configurator = BoardConfiguratorWidget()
        UiC().widgets.board_illuminator = BoardIlluminatorWidget()
        UiC().widgets.board_selector = BoardSelectorWidget()
        UiC().widgets.scan = ScanMainWidget()

        UiC().project_persistence = UiProjectPersistence()

        UiC().widgets.board_selector.boardSelected.connect(UiC().widgets.board_configurator.refresh)
        UiC().widgets.board_selector.boardSelected.connect(UiC().widgets.board_illuminator.load_from_client)
        UiC().widgets.board_selector.boardSelected.connect(UiC().widgets.scan.load_from_client)

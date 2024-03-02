from PySide6.QtWidgets import QWidget, QGridLayout

from pyside6helpers.group import make_group
from pyside6helpers.tab import make_tabs

from ledboarddesktopfull.components.board.configurator import BoardConfiguratorWidget
from ledboarddesktopfull.components.board.selector import BoardSelectorWidget
from ledboarddesktopfull.components.board.illuminator import BoardIlluminatorWidget
from ledboarddesktopfull.components.scan.main_widget import ScanMainWidget
from ledboarddesktopfull.core.components import Components


class CentralWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.board_configurator = BoardConfiguratorWidget()
        self.board_selector = BoardSelectorWidget()
        self.board_illuminator = BoardIlluminatorWidget()

        self.scan = ScanMainWidget()

        self.board_selector.boardSelected.connect(self.board_configurator.refresh)
        self.board_selector.boardSelected.connect(self.board_illuminator.load_from_client)

        layout = QGridLayout(self)
        layout.addWidget(make_group("Board selection",[self.board_selector]))
        layout.addWidget(make_group(
            "Board configuration",
            [self.board_configurator],
            fixed_width=Components().configuration.side_bar_width
        ))
        layout.addWidget(make_group("Simple illumination", [self.board_illuminator]))
        layout.addWidget(QWidget())

        layout.addWidget(make_tabs({
            "Scan": self.scan,
            "Layout": QWidget(),
            "Palettes": QWidget()
        }), 0, 1, 4, 1)

        layout.setRowStretch(3, 100)
        layout.setColumnStretch(1, 100)

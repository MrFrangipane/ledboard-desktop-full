from PySide6.QtWidgets import QWidget, QGridLayout

from pyside6helpers.group import make_group
from pyside6helpers.tab import make_tabs

from ledboarddesktopfull.components.board_configurator.widget import BoardConfiguratorWidget
from ledboarddesktopfull.components.board_selector.widget import BoardSelectorWidget
from ledboarddesktopfull.components.simple_illumination.widget import SimpleIlluminationWidget


class CentralWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.board_configurator = BoardConfiguratorWidget()

        self.board_selector = BoardSelectorWidget()
        self.board_selector.boardSelected.connect(self.board_configurator.refresh)

        self.illumination = SimpleIlluminationWidget()

        layout = QGridLayout(self)
        layout.addWidget(make_group("Board selection",[self.board_selector]))
        layout.addWidget(make_group("Board configuration", [self.board_configurator], fixed_width=300))
        layout.addWidget(make_group("Simple illumination",[self.illumination]))
        layout.addWidget(QWidget())

        layout.addWidget(make_tabs({
            "Scan": QWidget(),
            "Layout": QWidget(),
            "Palettes": QWidget()
        }), 0, 1, 4, 1)

        layout.setRowStretch(3, 100)
        layout.setColumnStretch(1, 100)

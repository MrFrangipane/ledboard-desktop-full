from PySide6.QtWidgets import QWidget, QGridLayout

from pyside6helpers.group import make_group

from ledboarddesktopfull.components.board_configurator.widget import BoardConfiguratorWidget
from ledboarddesktopfull.components.board_selector.widget import BoardSelectorWidget
from ledboarddesktopfull.components.gradient.widget.gradient_bar import GradientBarWidget
from ledboarddesktopfull.components.simple_illumination.widget import SimpleIlluminationWidget


class CentralWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.board_configurator = BoardConfiguratorWidget()

        self.board_selector = BoardSelectorWidget()
        self.board_selector.boardSelected.connect(self.board_configurator.refresh)

        self.gradient = GradientBarWidget()
        self.illumination = SimpleIlluminationWidget()

        layout = QGridLayout(self)
        layout.addWidget(make_group("Board selection",[self.board_selector]))
        layout.addWidget(make_group("Board configuration", [self.board_configurator]))
        layout.addWidget(make_group("Gradient editor",[self.gradient]))
        layout.addWidget(make_group("Simple illumination",[self.illumination]), 0, 1, 3, 1)

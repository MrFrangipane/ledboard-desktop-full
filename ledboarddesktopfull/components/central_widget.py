from PySide6.QtWidgets import QWidget, QGridLayout

from pyside6helpers.group import make_group
from pyside6helpers.tab import make_tabs

from ledboarddesktopfull.core.ui_components import UiComponents


class CentralWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QGridLayout(self)
        layout.addWidget(make_group("Board selection",[UiComponents().widgets.board_selector]))
        layout.addWidget(make_group(
            "Board configuration",
            [UiComponents().widgets.board_configurator],
            fixed_width=UiComponents().configuration.side_bar_width
        ))
        layout.addWidget(make_group("Simple illumination", [UiComponents().widgets.board_illuminator]))
        layout.addWidget(QWidget())

        layout.addWidget(make_tabs({
            "Scan": UiComponents().widgets.scan,
            "Layout": QWidget(),
            "Palettes": QWidget()
        }), 0, 1, 4, 1)

        layout.setRowStretch(3, 100)
        layout.setColumnStretch(1, 100)

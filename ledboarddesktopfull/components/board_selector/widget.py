from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QComboBox, QGridLayout, QPushButton
from pyside6helpers import combo, icons, hourglass
from ledboardclientfull import BoardConfiguration

from ledboarddesktopfull.core.components import Components


class BoardSelectorWidget(QWidget):
    boardSelected = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self._boards: [BoardConfiguration] = list()

        self.combo = QComboBox()
        self.combo.currentIndexChanged.connect(hourglass.hourglass_wrapper(self.board_selected))

        self.button_reload = QPushButton()
        self.button_reload.setIcon(icons.refresh())
        self.button_reload.setToolTip("Reload board list")
        self.button_reload.clicked.connect(hourglass.hourglass_wrapper(self._reload_board_list))
        self.button_reload.setFixedSize(24, 24)

        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.combo)
        layout.addWidget(self.button_reload, 0, 1)

    def _reload_board_list(self):
        self._boards = list(Components().board_api.available_boards())
        combo.update(self.combo, [f"{board_settings.name} ({port_name})" for port_name, board_settings in self._boards])

    def board_selected(self, index):
        port_name = self._boards[self.combo.currentIndex()][0]
        Components().board_api.set_serial_port(port_name)
        self.boardSelected.emit()

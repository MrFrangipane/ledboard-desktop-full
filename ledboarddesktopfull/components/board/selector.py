from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QComboBox, QGridLayout, QPushButton

from pyside6helpers import combo, icons, hourglass

from ledboardclientfull import BoardsList, board_api


class BoardSelectorWidget(QWidget):
    boardSelected = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self._dont_apply = 0
        self._boards_list = BoardsList()

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
        self._boards_list = board_api.available_boards()
        combo.update(self.combo, [f"{b.name} ({b.serial_port_name})" for b in self._boards_list.boards])

    def board_selected(self, index):
        if self._dont_apply > 0:
            return

        board_api.select_board(self._boards_list.boards[index])
        self.boardSelected.emit()

    def load_from_client(self):
        self._dont_apply += 1

        self._reload_board_list()
        current_board = board_api.get_selected_board()
        if current_board is not None:
            index = board_api.index_from_hardware_id(current_board.hardware_id)
            self.combo.setCurrentIndex(index)
        else:
            self.combo.setCurrentIndex(-1)

        self._dont_apply -= 1

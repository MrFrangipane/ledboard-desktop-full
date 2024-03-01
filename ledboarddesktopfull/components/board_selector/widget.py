from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QComboBox, QGridLayout, QPushButton

from pyside6helpers import combo, icons, hourglass

from ledboardclientfull import BoardsList, board

from ledboarddesktopfull.core.components import Components


class BoardSelectorWidget(QWidget):
    boardSelected = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

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

        Components().configuration.on_main_window_shown_callbacks.append(self._load_settings)

    def _reload_board_list(self):
        self._boards_list = board.available_boards()
        combo.update(self.combo, [f"{b.name} ({b.serial_port_name})" for b in self._boards_list.boards])

    def board_selected(self, index):
        board.select_board(self._boards_list.boards[index])
        self.boardSelected.emit()

    def _load_settings(self):
        self._reload_board_list()
        index = self._boards_list.index_from_hardware_id(board.get_selected_board().hardware_id)
        self.combo.setCurrentIndex(index)

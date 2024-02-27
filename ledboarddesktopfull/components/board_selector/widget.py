from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QComboBox, QGridLayout

from ledboarddesktopfull.core.components import Components


class BoardSelectorWidget(QWidget):
    boardSelected = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self._boards = list(Components().board_api.available_boards())

        self.combo = QComboBox()
        for port_name, board_settings in self._boards:
            self.combo.addItem(f"{board_settings.name} ({port_name})")
        self.combo.setCurrentIndex(-1)

        self.combo.currentIndexChanged.connect(self.board_selected)

        layout = QGridLayout(self)
        layout.addWidget(self.combo)

    def board_selected(self):
        port_name = self._boards[self.combo.currentIndex()][0]
        Components().board_api.set_serial_port(port_name)
        self.boardSelected.emit()

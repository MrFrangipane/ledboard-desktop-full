from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout

from pyside6helpers import icons


class ScanTools(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.button_mask = QPushButton("")
        self.button_mask.setToolTip("Masking")
        self.button_mask.setIcon(icons.screenshot())
        self.button_mask.setFixedSize(24, 24)
        self.button_mask.setCheckable(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.button_mask)

        layout.addWidget(QWidget())
        layout.setStretch(layout.count() - 1, 100)

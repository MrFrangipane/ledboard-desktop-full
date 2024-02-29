from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout

from pyside6helpers import icons


class ScanViewportTools(QWidget):
    maskEditingChanged = Signal(bool)
    maskResetClicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        #
        # Widgets
        self.button_mask_edit = QPushButton("Edit mask")
        self.button_mask_edit.setToolTip("Masking")
        self.button_mask_edit.setIcon(icons.screenshot())
        self.button_mask_edit.setCheckable(True)

        self.button_mask_reset = QPushButton("Reset mask")
        self.button_mask_reset.setToolTip("Masking")
        self.button_mask_reset.setIcon(icons.trash())

        #
        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.button_mask_edit)
        layout.addWidget(self.button_mask_reset)

        layout.addWidget(QWidget())
        layout.setStretch(layout.count() - 1, 100)

        #
        # Signals
        self.button_mask_edit.clicked.connect(self.maskEditingChanged)
        self.button_mask_reset.clicked.connect(self.maskResetClicked)

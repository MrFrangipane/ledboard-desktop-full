from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout

from pyside6helpers import icons
from pyside6helpers.frame import make_h_line


class ScanViewportTools(QWidget):
    maskEditingChanged = Signal(bool)
    maskResetClicked = Signal()
    maskToggleVisible = Signal(bool)
    fitClicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self._is_mask_visible = True

        #
        # Widgets
        self.button_fit_viewport = QPushButton("Fit view")
        self.button_fit_viewport.setIcon(icons.resize())
        self.button_fit_viewport.clicked.connect(self.fitClicked)

        self.button_mask_edit = QPushButton("Edit mask")
        self.button_mask_edit.setToolTip("Masking")
        self.button_mask_edit.setIcon(icons.screenshot())
        self.button_mask_edit.setCheckable(True)

        self.button_mask_toggle_visible = QPushButton("Hide mask")
        self.button_mask_toggle_visible.setIcon(icons.vision_stroked())
        self.button_mask_toggle_visible.clicked.connect(self._mask_toggle_visible)

        self.button_mask_reset = QPushButton("Reset mask")
        self.button_mask_reset.setToolTip("Masking")
        self.button_mask_reset.setIcon(icons.trash())

        #
        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.button_fit_viewport)
        layout.addWidget(make_h_line())
        layout.addWidget(self.button_mask_edit)
        layout.addWidget(self.button_mask_toggle_visible)
        layout.addWidget(self.button_mask_reset)

        layout.addWidget(QWidget())
        layout.setStretch(layout.count() - 1, 100)

        #
        # Signals
        self.button_mask_edit.clicked.connect(self.maskEditingChanged)
        self.button_mask_reset.clicked.connect(self.maskResetClicked)

    def _mask_toggle_visible(self):
        if self._is_mask_visible:
            self._is_mask_visible = False
            self.button_mask_toggle_visible.setIcon(icons.vision())
            self.button_mask_toggle_visible.setText("Show mask")
        else:
            self._is_mask_visible = True
            self.button_mask_toggle_visible.setIcon(icons.vision_stroked())
            self.button_mask_toggle_visible.setText("Hide mask")

        self.maskToggleVisible.emit(self._is_mask_visible)

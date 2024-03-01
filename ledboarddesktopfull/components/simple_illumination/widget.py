from PySide6.QtWidgets import QWidget, QLabel, QGridLayout

from pyside6helpers.slider import Slider
from ledboardclientfull import BoardIllumination, board, illumination


class SimpleIlluminationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.slider_start = Slider(minimum=0, maximum=500, on_value_changed=self._apply)
        self.slider_end = Slider(minimum=0, maximum=500, on_value_changed=self._apply)
        self.slider_single = Slider(minimum=0, maximum=500, on_value_changed=self._apply_single)

        self.slider_r = Slider(minimum=0, maximum=255, on_value_changed=self._apply)
        self.slider_g = Slider(minimum=0, maximum=255, on_value_changed=self._apply)
        self.slider_b = Slider(minimum=0, maximum=255, on_value_changed=self._apply)
        self.slider_w = Slider(minimum=0, maximum=255, on_value_changed=self._apply)

        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(QLabel("LED start"), 0, 0)
        layout.addWidget(self.slider_start, 0, 1)

        layout.addWidget(QLabel("LED end"), 1, 0)
        layout.addWidget(self.slider_end, 1, 1)

        layout.addWidget(QLabel("LED single"), 2, 0)
        layout.addWidget(self.slider_single, 2, 1)

        layout.addWidget(QLabel("Red"), 3, 0)
        layout.addWidget(self.slider_r, 3, 1)

        layout.addWidget(QLabel("Green"), 4, 0)
        layout.addWidget(self.slider_g, 4, 1)

        layout.addWidget(QLabel("Blue"), 5, 0)
        layout.addWidget(self.slider_b, 5, 1)

        layout.addWidget(QLabel("White"), 6, 0)
        layout.addWidget(self.slider_w, 6, 1)

    def _apply_single(self):
        # FIXME: figure out why signals are not blocked
        self.slider_start.blockSignals(True)
        self.slider_end.blockSignals(True)

        self.slider_start.setValue(self.slider_single.value())
        self.slider_end.setValue(self.slider_single.value())

        self.slider_start.blockSignals(False)
        self.slider_end.blockSignals(False)

    def _apply(self):
        illumination.illuminate(BoardIllumination(
            led_start=self.slider_start.value(),
            led_end=self.slider_end.value(),
            r=self.slider_r.value(),
            g=self.slider_g.value(),
            b=self.slider_b.value(),
            w=self.slider_w.value()
        ))

    def refresh(self):
        total_pixels = board.get_configuration().pixel_per_transmitter * 8
        self.slider_start.setRange(0, total_pixels)
        self.slider_end.setRange(0, total_pixels)
        self.slider_single.setRange(0, total_pixels)

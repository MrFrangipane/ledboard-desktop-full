from PySide6.QtWidgets import QWidget, QLabel, QGridLayout

from pyside6helpers.slider import Slider
from ledboardclientfull import BoardIllumination, board_api, illumination_api


class BoardIlluminatorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._dont_apply = 0

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
        self._dont_apply += 1

        self.slider_start.setValue(self.slider_single.value())
        self.slider_end.setValue(self.slider_single.value())

        self._dont_apply -= 1
        self._apply()

    def _apply(self):
        if self._dont_apply > 0:
            return

        illumination_api.illuminate(BoardIllumination(
            led_start=self.slider_start.value(),
            led_end=self.slider_end.value(),
            r=self.slider_r.value(),
            g=self.slider_g.value(),
            b=self.slider_b.value(),
            w=self.slider_w.value()
        ))

    def load_from_client(self):
        self._dont_apply += 1

        total_pixels = board_api.get_configuration().pixel_per_transmitter * 8  # get_configuration(), current_board() ?
        self.slider_start.setRange(0, total_pixels)
        self.slider_end.setRange(0, total_pixels)
        self.slider_single.setRange(0, total_pixels)

        illumination = illumination_api.get_illumination()
        self.slider_single.setValue(illumination.led_start)  # a bit hacky
        self.slider_end.setValue(illumination.led_end)
        self.slider_r.setValue(illumination.r)
        self.slider_g.setValue(illumination.g)
        self.slider_b.setValue(illumination.b)
        self.slider_w.setValue(illumination.w)

        self._dont_apply -= 1
        self._apply()

from PySide6.QtWidgets import QWidget, QLabel, QGridLayout, QRadioButton

from pyside6helpers.group import make_group_grid
from pyside6helpers.slider import Slider

from ledboardclientfull import BoardIllumination, BoardIlluminationType, board_api, illumination_api


class BoardIlluminatorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._dont_apply = 0

        self.radio_range = QRadioButton("Range")
        self.radio_range.toggled.connect(self._apply)
        self.slider_first = Slider(minimum=0, maximum=500, on_value_changed=self._apply)
        self.slider_last = Slider(minimum=0, maximum=500, on_value_changed=self._apply)

        self.radio_single = QRadioButton("Single")
        self.slider_single = Slider(minimum=0, maximum=500, on_value_changed=self._apply)

        self.slider_r = Slider(minimum=0, maximum=255, on_value_changed=self._apply)
        self.slider_g = Slider(minimum=0, maximum=255, on_value_changed=self._apply)
        self.slider_b = Slider(minimum=0, maximum=255, on_value_changed=self._apply)
        self.slider_w = Slider(minimum=0, maximum=255, on_value_changed=self._apply)

        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.radio_range, 0, 0, 1, 2)

        layout.addWidget(QLabel("LED start"), 1, 0)
        layout.addWidget(self.slider_first, 1, 1)

        layout.addWidget(QLabel("LED end"), 2, 0)
        layout.addWidget(self.slider_last, 2, 1)

        layout.addWidget(self.radio_single, 3, 0, 1, 2)

        layout.addWidget(QLabel("LED single"), 4, 0)
        layout.addWidget(self.slider_single, 4, 1)

        layout.addWidget(make_group_grid("Color", [
            [QLabel("Red"), self.slider_r],
            [QLabel("Green"), self.slider_g],
            [QLabel("Blue"), self.slider_b],
            [QLabel("White"), self.slider_w]
        ]), 5, 0, 1, 2)

    def _apply(self):
        if self._dont_apply > 0:
            return

        type_ = BoardIlluminationType.Range if self.radio_range.isChecked() else BoardIlluminationType.Single
        illumination_api.illuminate(BoardIllumination(
            type=type_,
            led_single=self.slider_single.value(),
            led_first=self.slider_first.value(),
            led_last=self.slider_last.value(),
            r=self.slider_r.value(),
            g=self.slider_g.value(),
            b=self.slider_b.value(),
            w=self.slider_w.value()
        ))

    def load_from_client(self):
        self._dont_apply += 1

        configuration = board_api.get_configuration()
        total_pixels = configuration.pixel_per_transmitter * 8  # get_configuration(), current_board() ?
        self.slider_first.setRange(0, total_pixels)
        self.slider_last.setRange(0, total_pixels)
        self.slider_single.setRange(0, total_pixels)

        illumination = illumination_api.get_illumination()
        self.radio_range.setChecked(illumination.type == BoardIlluminationType.Range)
        self.slider_first.setValue(illumination.led_first)
        self.slider_last.setValue(illumination.led_last)

        self.radio_single.setChecked(illumination.type == BoardIlluminationType.Single)
        self.slider_single.setValue(illumination.led_single)

        self.slider_r.setValue(illumination.r)
        self.slider_g.setValue(illumination.g)
        self.slider_b.setValue(illumination.b)
        self.slider_w.setValue(illumination.w)

        self._dont_apply -= 1
        self._apply()

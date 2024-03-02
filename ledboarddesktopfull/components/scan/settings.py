from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QPushButton, QCheckBox

from pyside6helpers import combo, icons
from pyside6helpers.group import make_group
from pyside6helpers.hourglass import hourglass_wrapper
from pyside6helpers.slider import Slider
from pyside6helpers.spinbox import SpinBox

from ledboardclientfull import board_api, illumination_api, scan_api

from ledboarddesktopfull.core.ui_components import UiComponents


class ScanSettingsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._dont_apply = 0

        #
        # Video input
        self.combo_video_inputs = QComboBox()
        self.combo_video_inputs.currentIndexChanged.connect(hourglass_wrapper(self.video_input_changed))

        self.button_refresh_video_inputs = QPushButton("")
        self.button_refresh_video_inputs.setIcon(icons.refresh())
        self.button_refresh_video_inputs.setFixedSize(24, 24)
        self.button_refresh_video_inputs.clicked.connect(hourglass_wrapper(self.refresh_video_inputs))

        #
        # Image Processing
        self.checkbox_viewport_brightest_pixel = QCheckBox("Show brightest pixel")
        self.checkbox_viewport_brightest_pixel.stateChanged.connect(self.brightest_pixel_changed)

        self.checkbox_viewport_blur = QCheckBox("Show blur")
        self.checkbox_viewport_blur.stateChanged.connect(self.is_live_blur_changed)

        self.slider_blur_radius = Slider(
            "Blur radius", minimum=0, maximum=8, on_value_changed=self.blur_radius_changed
        )

        #
        # LEDs
        self.spin_led_first = SpinBox("first", on_value_changed=self._apply)
        self.spin_led_last = SpinBox("last", on_value_changed=self._apply)
        self.button_led_range_from_illumination = QPushButton("From illumination range")
        self.button_led_range_from_illumination.clicked.connect(self._led_range_from_illumination)

        #
        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(make_group(
            "Video input",
            [
                self.combo_video_inputs,
                self.button_refresh_video_inputs
            ],
            orientation=Qt.Horizontal
        ))
        layout.addWidget(make_group(
            "Detection settings",
            [
                self.checkbox_viewport_brightest_pixel,
                self.checkbox_viewport_blur,
                self.slider_blur_radius
            ]
        ))
        layout.addWidget(make_group(
            "LEDs",
            widgets=[
                self.spin_led_first,
                self.spin_led_last,
                self.button_led_range_from_illumination
            ]
        ))
        layout.addWidget(QWidget())
        layout.setStretch(layout.count() - 1, 100)

        self.setFixedWidth(UiComponents().configuration.side_bar_width)

    def refresh_video_inputs(self):
        combo.update(self.combo_video_inputs, scan_api.get_capture_devices_names())

    def video_input_changed(self, index):
        if self._dont_apply > 0:
            return
        scan_api.set_capture_device(index)

    def is_live_blur_changed(self):
        if self._dont_apply > 0:
            return
        settings = scan_api.get_settings()
        settings.viewport_blur = self.checkbox_viewport_blur.isChecked()
        scan_api.set_settings(settings)

    def blur_radius_changed(self):
        if self._dont_apply > 0:
            return
        settings = scan_api.get_settings()
        settings.blur_radius = self.slider_blur_radius.value()
        scan_api.set_settings(settings)

    def brightest_pixel_changed(self):
        if self._dont_apply > 0:
            return
        settings = scan_api.get_settings()
        settings.viewport_brightest_pixel = self.checkbox_viewport_brightest_pixel.isChecked()
        scan_api.set_settings(settings)

    def load_from_client(self):
        self.refresh_video_inputs()
        self.combo_video_inputs.setCurrentIndex(scan_api.video_capture_index())

        self._dont_apply += 1

        scan_settings = scan_api.get_settings()
        self.checkbox_viewport_blur.setChecked(scan_settings.viewport_blur)
        self.checkbox_viewport_brightest_pixel.setChecked(scan_settings.viewport_brightest_pixel)
        self.slider_blur_radius.setValue(scan_settings.blur_radius)

        board_settings = board_api.get_selected_board()
        self.spin_led_first.setRange(0, board_settings.pixel_per_transmitter * 8)
        self.spin_led_first.setValue(scan_settings.led_first)
        self.spin_led_last.setRange(0, board_settings.pixel_per_transmitter * 8)
        self.spin_led_last.setValue(scan_settings.led_last)

        self._dont_apply -= 1

    def _led_range_from_illumination(self):
        self._dont_apply += 1
        illumination = illumination_api.get_illumination()
        self.spin_led_first.setValue(illumination.led_first)
        self.spin_led_last.setValue(illumination.led_last)
        self._dont_apply -= 1
        self._apply()

    def _apply(self):
        # FIXME: use this function for all widget changed
        if self._dont_apply > 0:
            return

        settings = scan_api.get_settings()
        settings.led_first = self.spin_led_first.value()
        settings.led_last = self.spin_led_last.value()
        scan_api.set_settings(settings)

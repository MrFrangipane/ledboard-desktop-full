from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QPushButton, QProgressBar, QCheckBox, QFileDialog

from pyside6helpers import combo, icons
from pyside6helpers.group import make_group
from pyside6helpers.hourglass import hourglass_wrapper
from pyside6helpers.slider import Slider
from pyside6helpers.spinbox import SpinBox

from ledboardclientfull import board_api, illumination_api, scan_api

from ledboarddesktopfull.core.ui_components import UiComponents


class ScanSideBar(QWidget):
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
        # Execution
        self.button_start = QPushButton("Start")
        self.button_start.setIcon(icons.play_button())
        self.button_start.clicked.connect(self._start_stop_scan)
        self.progress = QProgressBar()

        #
        # Export indexed led segments
        self.spin_segment_division_count = SpinBox("Segment division count", minimum=1, maximum=100, value=25)  # FIXME 25 for Blitz (5x25 < 128)
        self.spin_transmitter_index = SpinBox("Transmitter", minimum=1, maximum=8)
        self.button_export_indexed_led_segments = QPushButton("Export indexed LED segment...")
        self.button_export_indexed_led_segments.setIcon(icons.upload())
        self.button_export_indexed_led_segments.clicked.connect(self._export_indexed_led_segment)

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
        layout.addWidget(self.button_start)
        layout.addWidget(self.progress)

        layout.addWidget(QWidget())
        layout.setStretch(layout.count() - 1, 100)

        layout.addWidget(make_group(
            "Export",
            widgets=[
                self.spin_transmitter_index,
                self.spin_segment_division_count,
                self.button_export_indexed_led_segments
            ]
        ))

        self.setFixedWidth(UiComponents().configuration.side_bar_width)

    #
    # Widgets
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

    def _led_range_from_illumination(self):
        self._dont_apply += 1
        illumination = illumination_api.get_illumination()
        self.spin_led_first.setValue(illumination.led_first)
        self.spin_led_last.setValue(illumination.led_last)
        self._dont_apply -= 1
        self._apply()

    #
    # API update
    def load_from_client(self):
        self.refresh_video_inputs()
        self.combo_video_inputs.setCurrentIndex(scan_api.video_capture_index())

        self._dont_apply += 1

        scan_settings = scan_api.get_settings()
        self.checkbox_viewport_blur.setChecked(scan_settings.viewport_blur)
        self.checkbox_viewport_brightest_pixel.setChecked(scan_settings.viewport_brightest_pixel)
        self.slider_blur_radius.setValue(scan_settings.blur_radius)

        board_settings = board_api.get_selected_board()
        self.spin_led_first.setRange(0, board_settings.led_per_transmitter * 8)
        self.spin_led_first.setValue(scan_settings.led_first)
        self.spin_led_last.setRange(0, board_settings.led_per_transmitter * 8)
        self.spin_led_last.setValue(scan_settings.led_last)

        self._dont_apply -= 1

    def _apply(self):
        # FIXME: use this function for all widget changed
        if self._dont_apply > 0:
            return

        settings = scan_api.get_settings()
        settings.led_first = self.spin_led_first.value()
        settings.led_last = self.spin_led_last.value()
        scan_api.set_settings(settings)

    #
    # Scan
    def _start_stop_scan(self):
        if not scan_api.is_scanning():
            self._start_scan()
        else:
            self._stop_scan()

    def _start_scan(self):
        self.button_start.setText("Stop")
        self.button_start.setIcon(icons.stop())
        scan_settings = scan_api.get_settings()
        self.progress.setRange(scan_settings.led_first, scan_settings.led_last)

        UiComponents().widgets.scan.clear_detection_points()

        scan_api.start_scan()
        while scan_api.is_scanning():
            # FIXME : do this in a QThread
            scan_api.step_scan()
            self._update_progress()
            QApplication.processEvents()

        self._stop_scan()

    def _stop_scan(self):
        if scan_api.is_scanning():
            self.button_start.setText("Start")
            self.button_start.setIcon(icons.play_button())
            self.progress.setValue(0)
            scan_api.stop_scan()

    def _update_progress(self):
        self.progress.setValue(illumination_api.get_illumination().led_single)

    #
    # Export
    def _export_indexed_led_segment(self):
        # filename, _ = QFileDialog.getSaveFileName()
        # if not filename:
        #     return
        filename = "segment.json"

        scan_api.export_indexed_led_segment(
            filename=filename,
            transmitter=self.spin_transmitter_index.value(),
            division_count=self.spin_segment_division_count.value()
        )

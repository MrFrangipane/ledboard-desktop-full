from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QPushButton, QCheckBox

from pyside6helpers.group import make_group
from pyside6helpers import icons
from pyside6helpers.hourglass import hourglass_wrapper
from pyside6helpers import combo
from pyside6helpers.slider import Slider

from ledboarddesktopfull.core.components import Components


class ScanOptions(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

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
        layout.addWidget(QWidget())
        layout.setStretch(layout.count() - 1, 100)

        self.setFixedWidth(Components().configuration.side_bar_width)

        Components().configuration.on_main_window_shown_callbacks.append(self._load_settings)

    def refresh_video_inputs(self):
        combo.update(self.combo_video_inputs, Components().scan.image_processor.get_capture_devices_names())

    @staticmethod
    def video_input_changed(index):
        Components().scan.image_processor.set_capture_device(index)

    def is_live_blur_changed(self):
        Components().scan.image_processor.settings.viewport_blur = self.checkbox_viewport_blur.isChecked()

    def blur_radius_changed(self):
        Components().scan.image_processor.settings.blur_radius = self.slider_blur_radius.value()

    def brightest_pixel_changed(self):
        Components().scan.image_processor.settings.viewport_brightest_pixel = self.checkbox_viewport_brightest_pixel.isChecked()

    def _load_settings(self):
        self.refresh_video_inputs()
        self.combo_video_inputs.setCurrentIndex(Components().configuration.video_capture_index)

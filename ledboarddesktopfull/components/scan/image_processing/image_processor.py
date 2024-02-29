import cv2
import numpy as np
from numpy.typing import ArrayLike
from PySide6.QtGui import QPixmap, QImage

from ledboarddesktopfull.components.scan.image_processing.video_capture import VideoCapture
from ledboarddesktopfull.components.scan.image_processing.settings import ScanImageProcessingSettings


class ScanImageProcessor:
    def __init__(self):
        self._video_capture = VideoCapture()
        self.settings = ScanImageProcessingSettings()
        self._frame: ArrayLike = None
        self._mask: ArrayLike = None

    def get_capture_devices_names(self) -> list[str]:
        return self._video_capture.get_devices_names()

    def set_capture_device(self, device_index: int):
        self._video_capture.open(device_index)

    def set_scan_settings(self, settings: ScanImageProcessingSettings):
        self.settings = settings

    def reset_mask(self):
        if self._mask is not None:
            self._mask.fill(255)

    def set_mask(self, mask_geometry: ArrayLike):  # fixme use a dataclass
        self._mask = np.zeros(self._frame.shape[:2], dtype="uint8")
        cv2.fillPoly(self._mask, pts=[mask_geometry], color=(255, 255, 255))

    def viewport_pixmap(self):
        if not self._video_capture.is_open:
            return QPixmap()

        self._frame = self._video_capture.read()

        if self.settings.viewport_blur and self.settings.blur_radius > 0:
            blur = self.settings.blur_radius * 2 + 1
            self._frame = cv2.GaussianBlur(self._frame, (blur, blur), 0)

        self._frame = cv2.bitwise_and(self._frame, self._frame, mask=self._mask)

        if self.settings.viewport_brightest_pixel:
            gray = cv2.cvtColor(self._frame, cv2.COLOR_RGB2GRAY)  # is it BGR ?
            _, maximum_value, _, maximum_location = cv2.minMaxLoc(gray)
            cv2.circle(self._frame, maximum_location, 5, (255, 0, 0), -1)

        height, width, channel = self._frame.shape
        bytes_per_line = 3 * width
        qt_image = QImage(self._frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(qt_image)

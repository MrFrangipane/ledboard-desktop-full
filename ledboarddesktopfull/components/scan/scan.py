import cv2
from PySide6.QtGui import QPixmap, QImage

from ledboarddesktopfull.components.scan.image_processing.video_capture import VideoCapture
from ledboarddesktopfull.components.scan.scan_settings import ScanSettings


class Scan:
    def __init__(self):
        self._video_capture = VideoCapture()
        self.settings = ScanSettings()

    def get_capture_devices_names(self) -> list[str]:
        return self._video_capture.get_devices_names()

    def set_capture_device(self, device_index: int):
        self._video_capture.open(device_index)

    def set_scan_settings(self, settings: ScanSettings):
        self.settings = settings

    def viewport_pixmap(self):
        if not self._video_capture.is_open:
            return QPixmap()

        frame = self._video_capture.read()

        if self.settings.viewport_blur and self.settings.blur_radius > 0:
            blur = self.settings.blur_radius * 2 + 1
            frame = cv2.GaussianBlur(frame, (blur, blur), 0)

        if self.settings.viewport_brightest_pixel:
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)  # is it BGR ?
            _, maximum_value, _, maximum_location = cv2.minMaxLoc(gray)
            cv2.circle(frame, maximum_location, 5, (255, 0, 0), -1)

        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        qt_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(qt_image)

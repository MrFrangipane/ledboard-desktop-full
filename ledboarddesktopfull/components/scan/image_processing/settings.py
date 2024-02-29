from dataclasses import dataclass


@dataclass
class ScanImageProcessingSettings:
    viewport_blur: bool = False
    viewport_brightest_pixel: bool = False
    blur_radius: int = 0
    # FIXME : viewport framerate here ?

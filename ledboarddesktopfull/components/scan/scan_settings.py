from dataclasses import dataclass


@dataclass
class ScanSettings:
    viewport_blur: bool = False
    viewport_brightest_pixel: bool = False
    blur_radius: int = 0

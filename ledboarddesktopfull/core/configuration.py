from dataclasses import dataclass


@dataclass
class Configuration:
    resources_folder: str = None
    scan_viewport_framerate: int = 30
    side_bar_width: int = 260

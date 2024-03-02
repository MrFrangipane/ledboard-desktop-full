from typing import Callable
from dataclasses import dataclass, field


@dataclass
class Configuration:
    #
    # Constants
    resources_folder: str = None
    scan_viewport_framerate: int = 30
    side_bar_width: int = 260

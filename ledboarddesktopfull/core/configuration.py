from typing import Callable
from dataclasses import dataclass, field


@dataclass
class Configuration:
    #
    # Constants
    resources_folder: str = None
    scan_viewport_framerate: int = 30
    side_bar_width: int = 260

    #
    # Boot
    on_main_window_shown_callbacks: list[Callable] = field(default_factory=list)

    # FIXME: save / load from persistence
    board_index: int = 0
    video_capture_index: int = 0

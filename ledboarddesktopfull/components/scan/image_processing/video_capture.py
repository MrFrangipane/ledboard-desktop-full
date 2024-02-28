import logging
import subprocess
import sys

import imageio
import imageio_ffmpeg
from imageio.plugins.ffmpeg import CAM_FORMAT
from imageio.core.format import Format


_logger = logging.getLogger(__name__)


class VideoCapture:

    def __init__(self):
        self._capture: Format.Reader = None
        self.is_open = False

    def open(self, index):
        if self._capture is not None:
            self._capture.close()
            self.is_open = False

        self._capture = imageio.get_reader(f'<video{index}>')
        self.is_open = True

    def read(self):
        if self._capture is not None:
            return self._capture.get_next_data()

    @staticmethod
    def get_devices_names() -> list[str]:
        # FIXME: works onl for windows
        cmd = [
            imageio_ffmpeg.get_ffmpeg_exe(),
            "-list_devices",
            "true",
            "-f",
            CAM_FORMAT,
            "-i",
            "dummy",
        ]
        completed_process = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
            shell=True,
            check=False,
        )
        names = _parse_device_names(completed_process.stderr)
        return names


def _parse_device_names(ffmpeg_output):
    """Parse the output of the ffmpeg -list-devices command"""
    # Collect device names - get [friendly_name, alt_name] of each
    device_names = []
    in_video_devices = False
    for line in ffmpeg_output.splitlines():
        if line.startswith("[dshow"):
            line = line.split("]", 1)[1].strip()
            if in_video_devices and line.startswith('"'):
                friendly_name = line[1:-1]
                device_names.append([friendly_name, ""])
            elif in_video_devices and line.lower().startswith("alternative name"):
                alt_name = line.split(" name ", 1)[1].strip()[1:-1]
                if sys.platform.startswith("win"):
                    alt_name = alt_name.replace("&", "^&")  # Tested to work
                else:
                    alt_name = alt_name.replace("&", "\\&")  # Does this work?
                device_names[-1][-1] = alt_name
            elif "video devices" in line:
                in_video_devices = True
            elif "devices" in line:
                # set False for subsequent "devices" sections
                in_video_devices = False
    # Post-process, see #441
    # prefer friendly names, use alt name if two cams have same friendly name
    device_names2 = []
    for friendly_name, alt_name in device_names:
        if friendly_name not in device_names2:
            device_names2.append(friendly_name)
        elif alt_name:
            device_names2.append(alt_name)
        else:
            device_names2.append(friendly_name)  # duplicate, but not much we can do
    return device_names2

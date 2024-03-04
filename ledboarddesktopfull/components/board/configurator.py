from ipaddress import IPv4Address

from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QSpinBox, QComboBox, QPushButton
from pyside6helpers import icons

from ledboardclientfull import BoardExecutionMode, PixelType, board_api


class BoardConfiguratorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.line_name = QLineEdit()
        self.line_name.setMaxLength(7)

        self.line_ip_address = QLineEdit()

        self.spin_universe = QSpinBox()
        self.spin_universe.setRange(0, 15)

        self.spin_pixels_per_transmitter = QSpinBox()
        self.spin_pixels_per_transmitter.setRange(0, 500)

        self.combo_pixel_type = QComboBox()
        self.combo_pixel_type.addItems([item.name for item in PixelType])

        self.combo_execution_mode = QComboBox()
        self.combo_execution_mode.addItems([item.name for item in BoardExecutionMode])

        self.button_load_from_board = QPushButton("Load from board")
        self.button_load_from_board.setIcon(icons.refresh())
        self.button_load_from_board.clicked.connect(self.load_from_client)

        self.button_apply = QPushButton("Apply")
        self.button_apply.setIcon(icons.play_button())
        self.button_apply.clicked.connect(self.apply)

        self.label_hardware_revision = QLabel()
        self.label_hardware_id = QLabel()
        self.label_firmware_revision = QLabel()

        self.button_save_and_reboot = QPushButton("Save and reboot")
        self.button_save_and_reboot.setIcon(icons.diskette())
        self.button_save_and_reboot.clicked.connect(self.save_and_reboot)

        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(QLabel("Name"), 0, 0)
        layout.addWidget(self.line_name, 0, 1)

        layout.addWidget(QLabel("IP Address"), 1, 0)
        layout.addWidget(self.line_ip_address, 1, 1)

        layout.addWidget(QLabel("Artnet Universe"), 2, 0)
        layout.addWidget(self.spin_universe, 2, 1)

        layout.addWidget(QLabel("Pixels per transmitter"), 3, 0)
        layout.addWidget(self.spin_pixels_per_transmitter, 3, 1)

        layout.addWidget(QLabel("Pixel Type"), 4, 0)
        layout.addWidget(self.combo_pixel_type, 4, 1)

        layout.addWidget(QLabel("Execution Mode"), 5, 0)
        layout.addWidget(self.combo_execution_mode, 5, 1)

        layout.addWidget(QLabel("Firmware revision"), 6, 0)
        layout.addWidget(self.label_firmware_revision, 6, 1)

        layout.addWidget(QLabel("Hardware revision"), 7, 0)
        layout.addWidget(self.label_hardware_revision, 7, 1)

        layout.addWidget(QLabel("Hardware ID"), 8, 0)
        layout.addWidget(self.label_hardware_id, 8, 1)

        layout.addWidget(self.button_load_from_board, 9, 0, 1, 2)
        layout.addWidget(self.button_apply, 10, 0, 1, 2)
        layout.addWidget(self.button_save_and_reboot, 11, 0, 1, 2)

    def load_from_client(self):
        configuration = board_api.get_configuration()

        self.line_name.setText(configuration.name.strip())
        self.line_ip_address.setText(str(configuration.ip_address))
        self.spin_universe.setValue(configuration.universe_a) # FIXME there are 3 universes now
        self.spin_pixels_per_transmitter.setValue(configuration.led_per_transmitter)
        self.combo_pixel_type.setCurrentIndex(configuration.pixel_type.value)
        self.combo_execution_mode.setCurrentIndex(configuration.execution_mode.value)

        self.label_firmware_revision.setText(str(configuration.firmware_revision))
        self.label_hardware_id.setText(configuration.hardware_id)
        self.label_hardware_revision.setText(str(configuration.hardware_revision))

    def save_and_reboot(self):
        self._send(save=True)

    def apply(self):
        self._send(save=False)

    def _send(self, save):
        configuration = board_api.get_selected_board()

        configuration.name = self.line_name.text()
        configuration.execution_mode = BoardExecutionMode(self.combo_execution_mode.currentIndex())
        configuration.ip_address = IPv4Address(self.line_ip_address.text())
        configuration.universe_a = self.spin_universe.value()
        configuration.led_per_transmitter = self.spin_pixels_per_transmitter.value()
        configuration.pixel_type = PixelType(self.combo_pixel_type.currentIndex())
        configuration.do_save_and_reboot = save

        board_api.set_configuration(configuration)

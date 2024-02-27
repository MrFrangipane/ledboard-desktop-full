from ipaddress import IPv4Address

from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QSpinBox, QComboBox, QPushButton

from ledboarddesktopfull.core.components import Components


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
        self.combo_pixel_type.addItems(["GRBW", "GRB"])

        self.button_apply = QPushButton("Apply")
        self.button_apply.clicked.connect(self.apply)

        self.button_save_and_reboot = QPushButton("Save and reboot")
        self.button_save_and_reboot.clicked.connect(self.save_and_reboot)

        layout = QGridLayout(self)
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

        layout.addWidget(self.button_apply, 5, 0, 1, 2)
        layout.addWidget(self.button_save_and_reboot, 6, 0, 1, 2)

    def refresh(self):
        configuration = Components().board_api.get_configuration()
        print(configuration)
        self.line_name.setText(configuration.name.strip())
        self.line_ip_address.setText(str(configuration.ip_address))
        self.spin_universe.setValue(configuration.universe)
        self.spin_pixels_per_transmitter.setValue(configuration.pixel_per_transmitter)
        self.combo_pixel_type.setCurrentIndex(int(configuration.pixel_type))

    def save_and_reboot(self):
        self._send(save=True)

    def apply(self):
        self._send(save=False)

    def _send(self, save):
        configuration = Components().board_api.get_configuration()

        configuration.name = self.line_name.text()
        configuration.ip_address = IPv4Address(self.line_ip_address.text())
        configuration.universe = self.spin_universe.value()
        configuration.pixel_per_transmitter = self.spin_pixels_per_transmitter.value()
        configuration.pixel_type = self.combo_pixel_type.currentIndex()
        configuration.do_save_and_reboot = save

        Components().board_api.set_configuration(configuration)

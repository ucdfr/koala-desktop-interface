__author__ = 'yilu'

from PyQt4.QtGui import *

class ServerStatusDisplay(QWidget):
    def __init__(self):
        super(ServerStatusDisplay, self).__init__()

        self.main_layout = QVBoxLayout()

        self.first_vbox = QHBoxLayout()
        self.host_name_label = QLabel("Server host:")
        self.host_label = QLabel("127.0.0.1")
        self.first_vbox.addWidget(self.host_name_label)
        self.first_vbox.addWidget(self.host_label)
        self.first_vbox.addStretch(1)
        self.main_layout.addLayout(self.first_vbox)

        self.second_vbox = QHBoxLayout()
        self.connection_status_name_label = QLabel("Connection Status:")
        self.connection_status_label = QLabel("Not Connected")
        self.second_vbox.addWidget(self.connection_status_name_label)
        self.second_vbox.addWidget(self.connection_status_label)
        self.second_vbox.addStretch(1)
        self.main_layout.addLayout(self.second_vbox)

        self.setLayout(self.main_layout)
        self.setAutoFillBackground(True)
        self.setStyleSheet("background-color:red;")
        # p = self.palette()
        # p.setColor(self.backgroundRole(), Qt.red)
        # self.setPalette(p)

    def set_host(self, host):
        self.host_label.setText(host)

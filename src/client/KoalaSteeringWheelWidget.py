__author__ = 'yilu'

from PyQt4.QtGui import *
from PyQt4.QtCore import *


class KoalaSteeringWheel(QWidget):

    def __init__(self):
        super(KoalaSteeringWheel, self).__init__()
        self.image = QImage()
        self.arrowView = KoalaSteeringWheelArrow()


class KoalaSteeringWheelArrow(QWidget):
    def __init__(self):
        super(KoalaSteeringWheelArrow, self).__init__()
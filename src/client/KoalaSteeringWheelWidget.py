__author__ = 'yilu'

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import imageResources


class KoalaSteeringWheel(QWidget):

    def __init__(self):
        super(KoalaSteeringWheel, self).__init__()
        self.scene = QGraphicsScene()
        self.view = QGraphicsView()
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

        self.scene.setSceneRect(0, 0, 150, 150)
        self.image = QPixmap(':/images/steeringWheel.png').scaledToWidth(150).scaledToHeight(150)
        self.scene.addPixmap(self.image)
        self.view.setScene(self.scene)

    def paintEvent(self, paint_event):
        print "paint event trigger"
        testColor = QColor(255, 0, 0)
        rect = QRectF(0.0, 0.0, 100.0, 100.0)
        startAngle = 30 * 16
        spanAngle = 120 * 16
        painter = QPainter()
        painter.begin(self)
        painter.setPen(Qt.red)
        painter.setBrush(testColor)
        painter.drawArc(rect, startAngle, spanAngle)
        painter.drawLine(88, 0, 96, 0)
        painter.end()


class KoalaSteeringWheelArrow(QWidget):
    def __init__(self):
        super(KoalaSteeringWheelArrow, self).__init__()
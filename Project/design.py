from pickle import FALSE
from re import T
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import math


class Design(QWidget):
    def __init__(self, *args):
        super(Design, self).__init__()
        uic.loadUi('main.ui', self)

        # Fix the size of the widget
        self.setFixedSize(self.geometry().width(), self.geometry().height())

        self.startBtn.clicked.connect(self.start)
        self.finishBtn.clicked.connect(self.close)
        self.resetBtn.clicked.connect(self.reset)
        self.estimateBtn.clicked.connect(self.estimate)
        
        self.show()

        # The list that saves the coordinates of the points
        self.x_co = []
        self.y_co = []

        # The distance of each node
        self.distances = []

        # k most central nodes
        self.k_central_nodes = []

        self.bStarted = False
        self.bEstimated = False

        # Mouse event not working in groupbox
        self.groupBox_x = self.groupBox.pos().x()
        self.groupBox_y = self.groupBox.pos().y()

        # The radius of the circle representing k central nodes
        self.k_central_radius = 15
        
        QObject.startTimer(self, 300)

    def mousePressEvent(self, event):
        if self.bStarted is False:
            return

        if event.pos().x() > self.groupBox_x - 10 and event.pos().y() > self.groupBox_y - 10:
            return

        if event.button() == Qt.LeftButton:
            self.x_co.append(event.pos().x())
            self.y_co.append(event.pos().y())
            self.update()   

    # Pointing Function
    def start(self):
        self.bStarted = True
        self.startBtn.setEnabled(False)

    def reset(self):
        self.x_co.clear()
        self.y_co.clear()
        self.distances.clear()
        self.k_central_nodes.clear()
        self.bEstimated = False
        self.bStarted = False
        self.update()
        self.startBtn.setEnabled(True)
        self.estimateBtn.setEnabled(True)
        self.k.setEnabled(True)

    def estimate(self):

        if self.k.text() == '':
            QMessageBox(QMessageBox.Warning, 'warning', 'Please enter the value of k!').exec()
            return

        if(int(self.k.text()) > len(self.x_co)):
            QMessageBox(QMessageBox.Warning, "warning", "k must be smaller than the number of nodes").exec()
            return
        
        self.estimateBtn.setEnabled(False)
        self.k.setEnabled(False)

        for i in range(len(self.x_co)):
            distance = 0.0
            for j in range(len(self.x_co)):
                distance += self.getDistance(self.x_co[i], self.y_co[i], self.x_co[j], self.y_co[j])

            self.distances.append(distance)

        # Sort distances

        distances_copy = []
        for index in range(len(self.distances)):
            distances_copy.append(self.distances[index])

        for i in range(len(distances_copy) - 1):
            for j in range(i + 1, len(distances_copy)):
                if(distances_copy[i] > distances_copy[j]):
                    temp = distances_copy[i]
                    distances_copy[i] = distances_copy[j]
                    distances_copy[j] = temp

        for i in range(int(self.k.text())):
            self.k_central_nodes.append(self.distances.index(distances_copy[i]))

        self.bEstimated = True
        self.update()

    def getDistance(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def timerEvent(self, event):
        self.k_central_radius += 5

        if self.k_central_radius >= 30:
            self.k_central_radius = 15
        
        self.update()

    def paintEvent(self, event):
        pa = QPainter(self)
        pen = QPen()
        
        color = QColor(Qt.black)
        pen.setColor(color)
        pa.setPen(pen)
        pa.setBrush(Qt.green)

        for i in range(len(self.x_co)):
            pa.drawEllipse(self.x_co[i] - 4, self.y_co[i] - 4, 8, 8)

        if self.bEstimated is True:

            pen.setStyle(Qt.DashDotDotLine)
            pa.setPen(pen)
            pa.setBrush(Qt.NoBrush)

            for i in range(len(self.k_central_nodes)):
                pa.drawEllipse(self.x_co[self.k_central_nodes[i]] - self.k_central_radius,
                               self.y_co[self.k_central_nodes[i]] - self.k_central_radius,
                               self.k_central_radius * 2, 
                               self.k_central_radius * 2)
        pa.end()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = Design()
    form.show()
    app.exec()



       


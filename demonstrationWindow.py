import numpy as np
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel
import sys
from PyQt5.QtGui import QPixmap
import json


from UICircle import *

monitor_width = 1280
monitor_height = 860

class Window(QDialog):
    current = 0
    savedData = []
    def __init__(self):
        super().__init__()
        self.title = "Demonstration"
        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)

        self.setFixedSize(monitor_width, monitor_height)


        with open('09_06_2021_09_16_49.json') as f:
            self.savedData = json.load(f)

        vbox = QVBoxLayout()

        self.labelImage = QLabel(self)
        self.pixmap = QPixmap("besedila-1.jpg")
        self.pixmap = self.pixmap.scaled(monitor_width, monitor_height)

        self.labelImage.setPixmap(self.pixmap)
        vbox.addWidget(self.labelImage)

        self.circle = UICircle(self)

        self.setLayout(vbox)
        self.show()

        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.movePoint)
        self.timer.start()

    def movePoint(self):
        if self.savedData[int(self.current)] != [None]:

            point = self.savedData[int(self.current)]
            if point["left_gaze_point_validity"] == 1 and point["right_gaze_point_validity"] == 1:
                left = point["left_gaze_point_on_display_area"]
                right = point["right_gaze_point_on_display_area"]

                xs = (left[0], right[0])
                ys = (left[1], right[1])

                # if all of the axes have data from at least one eye
                if not (np.isnan(xs)).all() or not (np.isnan(ys)).all():
                    avgEyePos = (np.nanmean(xs), np.nanmean(ys))
                else:
                    avgEyePos = (0, 0, 0)

                self.circle.move(avgEyePos[0] * monitor_width, avgEyePos[1] * monitor_height)
            else:
                print("not")

        self.current = int(self.current) + int(1)






App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
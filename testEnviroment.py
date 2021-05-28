import sys
import rpyc

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from EyeTrackerService import *

from UICircle import *
from calibrationWindow import UIEyeLocationCircle

from FileSave import *

widthScreen = 1920
heightScreen = 1080


class WorkerThread(QThread):
    updateProgress = pyqtSignal(int)
    proxy = None
    data_buffer = []

    def __init__(self):
        super().__init__()
        print("init worker")
        # self.proxy = rpyc.connect('localhost', 33333, config={'allow_public_attrs': True})

    def run(self):
        self.tracker = EyeTracker()
        self.tracker.start_tracking()

        self.fileSaver = FileSave()

        self.calibration = tr.ScreenBasedCalibration(self.tracker.tracker)
        self.calibration.enter_calibration_mode()

        # result = self.proxy.root.turn_on_eyetracker_capture()
        #
        # while True:
        #     self.data_buffer.append(self.tracker.get_data())
        #     time.sleep(0.1)

    def stop(self):
        print("worker stop")
        self.tracker.stop_tracking()
        # result = self.proxy.root.turn_on_eyetracker_capture('C:\\Users\\PC\Desktop\\tests\\test123.json')
        # self.terminate()


class UITestPoints(QWidget):
    currentIndex = 0
    points_to_test = [(0.1, 0.1), (0.1, 0.9), (0.5, 0.5), (0.9, 0.1), (0.9, 0.9)]
    currentPoint = None,
    dots_on_screen = []
    eye_position_on_screen = []
    worker = None

    def __init__(self, parent=None):
        super(UITestPoints, self).__init__(parent)

        self.vbox = QVBoxLayout()
        self.vbox.setAlignment(Qt.AlignCenter)
        self.setLayout(self.vbox)

        self.currentPoint = UICircle(self)
        self.currentPoint.hide()

        self.saveBtn = QPushButton('Save', self)
        self.saveBtn.move(int(widthScreen * 0.6), int(heightScreen * 0.9))
        self.saveBtn.clicked.connect(self.save_data)
        self.saveBtn.hide()

        self.discardBtn = QPushButton('Discard', self)
        self.discardBtn.move(int(widthScreen * 0.4), int(heightScreen * 0.9))
        self.discardBtn.clicked.connect(self.discard_data)
        self.discardBtn.hide()

        self.worker = WorkerThread()
        self.worker.start()

        print("done init")

    def move_test_point(self):
        if self.currentIndex > 0:
            currentPoint = self.points_to_test[self.currentIndex - 1]

            result = self.worker.calibration.collect_data(currentPoint[0], currentPoint[1])
            if result != tr.CALIBRATION_STATUS_SUCCESS:
                print("not ok")
            else:
                print("ok")

        if self.currentIndex >= len(self.points_to_test):
            self.timer.stop()
            self.apply_save_calibration()
            return

        correctPoint = self.points_to_test[self.currentIndex]
        self.currentPoint.move(int(widthScreen * correctPoint[0]), int(heightScreen * correctPoint[1]))
        self.currentPoint.show()
        self.currentIndex = int(self.currentIndex) + 1

    def apply_save_calibration(self):
        self.dots_on_screen = []
        for dot in self.points_to_test:
            newDot = UICircle(self)
            newDot.move(int(widthScreen * dot[0]), int(heightScreen * dot[1]))
            newDot.show()
            self.dots_on_screen.append(newDot)

        calibration_result = self.worker.calibration.compute_and_apply()

        print("Compute and apply returned {0} and collected at {1} points.".format(calibration_result.status, len(
            calibration_result.calibration_points)))

        # data_to_save = {}
        for point in calibration_result.calibration_points:
            eyes_position = point.calibration_samples[0]


            left_eye = eyes_position.left_eye
            right_eye = eyes_position.right_eye

            left_eye_circle = UIEyeLocationCircle(self)
            left_eye_circle.move(int(left_eye.position_on_display_area[0] * widthScreen),
                                 int(left_eye.position_on_display_area[1] * heightScreen))
            left_eye_circle.show()

            right_eye_circle = UIEyeLocationCircle(self)
            right_eye_circle.move(int(right_eye.position_on_display_area[0] * widthScreen),
                                  int(right_eye.position_on_display_area[1] * heightScreen))
            right_eye_circle.show()

            # data_to_save[point.position_on_display_area] = {
            #     "left_eye": (left_eye.position_on_display_area[0], left_eye.position_on_display_area[1]),
            #     "right_eye": (right_eye.position_on_display_area[0], right_eye.position_on_display_area[1])
            # }
            #

            # print(data_to_save)
            self.worker.fileSaver.addToDataCollection({
                'position': point.position_on_display_area,
                "left_eye": (left_eye.position_on_display_area[0], left_eye.position_on_display_area[1]),
                "right_eye": (right_eye.position_on_display_area[0], right_eye.position_on_display_area[1])
            })



            # self.eye_position_on_screen.append(left_eye_circle)
            # self.eye_position_on_screen.append(right_eye_circle)

        # self.worker.fileSaver.data_collection = data_to_save

        self.saveBtn.show()
        self.discardBtn.show()

    def discard_data(self):
        print("discarding data")
        self.worker.calibration.leave_calibration_mode()
        self.worker.stop()
        w.startStartingMenu()

    def save_data(self):
        print("saving data")
        self.worker.calibration.leave_calibration_mode()
        self.worker.fileSaver.saveDataToFile()
        self.worker.stop()
        w.startStartingMenu()


class UIStartingMenu(QWidget):
    def __init__(self, parent=None):
        super(UIStartingMenu, self).__init__(parent)

        self.vbox = QVBoxLayout()
        self.vbox.setAlignment(Qt.AlignCenter)

        self.startTestBtn = QPushButton('Start test', self)
        self.exitBtn = QPushButton('Exit', self)
        self.vbox.addWidget(self.startTestBtn)
        self.vbox.addWidget(self.exitBtn)
        self.setLayout(self.vbox)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.showFullScreen()
        self.startStartingMenu()

    def startStartingMenu(self):
        self.StartingMenu = UIStartingMenu(self)
        self.setCentralWidget(self.StartingMenu)
        self.StartingMenu.startTestBtn.clicked.connect(self.startTest)
        self.StartingMenu.exitBtn.clicked.connect(self.closeApplication)
        self.show()

    def startTest(self):
        self.TestPoints = UITestPoints(self)
        self.setWindowTitle("Test")
        self.setCentralWidget(self.TestPoints)

        self.show()
        self.TestPoints.timer = QTimer()
        self.TestPoints.timer.setInterval(2000)
        self.TestPoints.timer.timeout.connect(self.TestPoints.move_test_point)

        self.TestPoints.timer.start()

    def closeApplication(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())

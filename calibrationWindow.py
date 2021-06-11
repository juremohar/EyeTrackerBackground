import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from EyeTrackerService import *

from UICircle import *


from win32api import GetSystemMetrics

widthScreen = GetSystemMetrics(0)
heightScreen = GetSystemMetrics(1)


class WorkerThread(QThread):
    updateProgress = pyqtSignal(int)

    def run(self):
        self.tracker = EyeTracker()
        self.tracker.start_tracking()

        self.calibration = tr.ScreenBasedCalibration(self.tracker.tracker)
        self.calibration.enter_calibration_mode()

        while True:
            time.sleep(0.1)

    def stop(self):
        print("worker stop")
        self.tracker.stop_tracking()
        self.terminate()


class UIEyeLocationCircle(QWidget):
    def __init__(self, parent=None):
        super(UIEyeLocationCircle, self).__init__(parent)

        self.circle = QLabel(self)
        self.circle.resize(5, 5)
        self.circle.setStyleSheet("background-color: green; border: 1px solid green; border-radius: 3px;")


class UICalibrate(QWidget):
    currentIndex = 0
    # points_to_calibrate = [(0.1, 0.1), (0.1, 0.5), (0.1, 0.9), (0.5, 0.1), (0.5, 0.5), (0.5, 0.9), (0.9, 0.1),
    #                        (0.9, 0.5), (0.9, 0.9)]
    points_to_calibrate = [(0.1, 0.1), (0.1, 0.9), (0.5, 0.5), (0.9, 0.1), (0.9, 0.9)]
    currentPoint = None,
    dots_on_screen = []
    eye_position_on_screen = []

    def __init__(self, parent=None):
        super(UICalibrate, self).__init__(parent)

        self.vbox = QVBoxLayout()
        self.vbox.setAlignment(Qt.AlignCenter)
        self.setLayout(self.vbox)

        self.currentPoint = UICircle(self)
        self.currentPoint.hide()

        self.discardBtn = QPushButton('Discard', self)
        self.discardBtn.move(int(widthScreen * 0.4), int(heightScreen * 0.9))
        self.discardBtn.clicked.connect(self.discardCalibration)
        self.discardBtn.hide()

        self.saveApplyBtn = QPushButton('Save & Apply', self)
        self.saveApplyBtn.move(int(widthScreen * 0.6), int(heightScreen * 0.9))
        self.saveApplyBtn.clicked.connect(self.leaveCalibrationMode)
        self.saveApplyBtn.hide()

        self.worker = WorkerThread()
        self.worker.start()

        print("done init")

    def moveCalibrationPoint(self):
        if self.currentIndex > 0:
            currentPoint = self.points_to_calibrate[self.currentIndex - 1]

            result = self.worker.calibration.collect_data(currentPoint[0], currentPoint[1])
            if result != tr.CALIBRATION_STATUS_SUCCESS:
                print("not ok")
            else:
                print("ok")

        if self.currentIndex >= len(self.points_to_calibrate):
            self.timer.stop()
            self.applySaveCalibration()
            return

        correctPoint = self.points_to_calibrate[self.currentIndex]
        self.currentPoint.move(int(widthScreen * correctPoint[0]), int(heightScreen * correctPoint[1]))
        self.currentPoint.show()
        self.currentIndex = int(self.currentIndex) + 1

    def discardCalibration(self):
        self.worker.calibration.leave_calibration_mode()
        self.worker.stop()
        w.startStartingMenu()

    def applySaveCalibration(self):

        self.dots_on_screen = []
        for dot in self.points_to_calibrate:
            newDot = UICircle(self)
            newDot.move(int(widthScreen * dot[0]), int(heightScreen * dot[1]))
            newDot.show()
            self.dots_on_screen.append(newDot)

        self.discardBtn.show()
        self.saveApplyBtn.show()

        calibration_result = self.worker.calibration.compute_and_apply()

        print("Compute and apply returned {0} and collected at {1} points.".format(calibration_result.status, len(
            calibration_result.calibration_points)))

        for point in calibration_result.calibration_points:
            pos_display_area = point.position_on_display_area
            eyes_position = point.calibration_samples[0]

            left_eye = eyes_position.left_eye
            right_eye = eyes_position.right_eye

            print(left_eye.position_on_display_area[0], left_eye.position_on_display_area[1])
            print(right_eye.position_on_display_area)

            left_eye_circle = UIEyeLocationCircle(self)
            left_eye_circle.move(int(left_eye.position_on_display_area[0] * widthScreen),
                                 int(left_eye.position_on_display_area[1] * heightScreen))
            left_eye_circle.show()

            right_eye_circle = UIEyeLocationCircle(self)
            right_eye_circle.move(int(right_eye.position_on_display_area[0] * widthScreen),
                                  int(right_eye.position_on_display_area[1] * heightScreen))
            right_eye_circle.show()

            self.eye_position_on_screen.append(left_eye_circle)
            self.eye_position_on_screen.append(right_eye_circle)

        # self.worker.calibration.leave_calibration_mode()
        # self.worker.stop()
        # w.startStartingMenu()

    def leaveCalibrationMode(self):
        self.worker.calibration.leave_calibration_mode()
        self.worker.stop()
        w.startStartingMenu()


class UIStartingMenu(QWidget):
    def __init__(self, parent=None):
        super(UIStartingMenu, self).__init__(parent)

        self.vbox = QVBoxLayout()
        self.vbox.setAlignment(Qt.AlignCenter)

        self.calibrateBtn = QPushButton('Start calibration', self)
        self.exitBtn = QPushButton('Exit', self)
        self.vbox.addWidget(self.calibrateBtn)
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
        self.StartingMenu.calibrateBtn.clicked.connect(self.startUICalibration)
        self.StartingMenu.exitBtn.clicked.connect(self.closeApplication)
        self.show()

    def startUICalibration(self):
        self.Calibrate = UICalibrate(self)
        self.setWindowTitle("Calibrate")
        self.setCentralWidget(self.Calibrate)

        self.show()

        self.Calibrate.timer = QTimer()
        self.Calibrate.timer.setInterval(2000)
        self.Calibrate.timer.timeout.connect(self.Calibrate.moveCalibrationPoint)

        self.Calibrate.timer.start()

    def closeApplication(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())

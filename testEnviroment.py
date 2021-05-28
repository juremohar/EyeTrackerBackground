import sys
import rpyc

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from EyeTrackerService import *

from UICircle import *

widthScreen = 1920
heightScreen = 1080


class WorkerThread(QThread):
    updateProgress = pyqtSignal(int)
    proxy = None
    data_buffer = []

    def __init__(self):
        super().__init__()
        print("init worker")
        self.proxy = rpyc.connect('localhost', 33333, config={'allow_public_attrs': True})

    def run(self):
        self.tracker = EyeTracker()
        self.tracker.start_tracking()

        result = self.proxy.root.turn_on_eyetracker_capture()

        while True:
            self.data_buffer.append(self.tracker.get_data())
            time.sleep(0.1)


    def stop(self):
        print("worker stop")
        self.tracker.stop_tracking()
        result = self.proxy.root.turn_on_eyetracker_capture('C:\\Users\\PC\Desktop\\tests\\test123.json')
        self.terminate()

    def return_and_empty_buffer(self):
        tmp = self.data_buffer
        self.data_buffer = []
        return tmp

    def empty_buffer(self):
        self.data_buffer = []


class UITestPoints(QWidget):
    currentIndex = 0
    points_to_test = [(0.1, 0.1), (0.1, 0.9), (0.5, 0.5), (0.9, 0.1), (0.9, 0.9)]
    currentPoint = None,
    dots_on_screen = []
    eye_position_on_screen = []

    def __init__(self, parent=None):
        super(UITestPoints, self).__init__(parent)

        self.vbox = QVBoxLayout()
        self.vbox.setAlignment(Qt.AlignCenter)
        self.setLayout(self.vbox)

        self.currentPoint = UICircle(self)
        self.currentPoint.hide()

        self.worker = WorkerThread()
        self.worker.start()

        print("done init")

    def move_test_point(self):
        if self.currentIndex > 0:
            currentPoint = self.points_to_test[self.currentIndex - 1]

        if self.currentIndex >= len(self.points_to_test):
            self.timer.stop()
            self.applySaveCalibration()
            # self.dots_on_screen = []
            # for dot in self.points_to_test:
            #     newDot = UICircle(self)
            #     newDot.move(int(widthScreen * dot[0]), int(heightScreen * dot[1]))
            #     newDot.show()
            #     self.dots_on_screen.append(newDot)
            #     self.applySaveCalibration()
            # self.discardBtn.show()
            # self.saveApplyBtn.show()
            return

        correctPoint = self.points_to_test[self.currentIndex]
        self.currentPoint.move(int(widthScreen * correctPoint[0]), int(heightScreen * correctPoint[1]))
        self.currentPoint.show()
        self.currentIndex = int(self.currentIndex) + 1

    def applySaveCalibration(self):

        self.dots_on_screen = []
        for dot in self.points_to_test:
            newDot = UICircle(self)
            newDot.move(int(widthScreen * dot[0]), int(heightScreen * dot[1]))
            newDot.show()
            self.dots_on_screen.append(newDot)

        self.discardBtn.show()
        self.saveApplyBtn.show()

        calibration_result = self.worker.calibration.compute_and_apply()

        print("Compute and apply returned {0} and collected at {1} points.".format(calibration_result.status, len(
            calibration_result.calibration_points)))

        # for point in calibration_result.calibration_points:
        #     pos_display_area = point.position_on_display_area
        #     eyes_position = point.calibration_samples[0]
        #
        #     left_eye = eyes_position.left_eye
        #     right_eye = eyes_position.right_eye
        #
        #     print(left_eye.position_on_display_area[0], left_eye.position_on_display_area[1])
        #     print(right_eye.position_on_display_area)
        #
        #     left_eye_circle = UIEyeLocationCircle(self)
        #     left_eye_circle.move(int(left_eye.position_on_display_area[0] * widthScreen),
        #                          int(left_eye.position_on_display_area[1] * heightScreen))
        #     left_eye_circle.show()
        #
        #     right_eye_circle = UIEyeLocationCircle(self)
        #     right_eye_circle.move(int(right_eye.position_on_display_area[0] * widthScreen),
        #                           int(right_eye.position_on_display_area[1] * heightScreen))
        #     right_eye_circle.show()
        #
        #     self.eye_position_on_screen.append(left_eye_circle)
        #     self.eye_position_on_screen.append(right_eye_circle)

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

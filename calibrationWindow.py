import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from EyeTrackerService import *

widthScreen = 1920
heightScreen = 1080


class WorkerThread(QThread):
    updateProgress = pyqtSignal(int)

    def run(self):
        self.tracker = EyeTracker()
        self.tracker.start_tracking()

        self.calibration = tr.ScreenBasedCalibration(self.tracker.tracker)
        self.calibration.enter_calibration_mode()

        while True:
            data = self.tracker.get_data()
            # print(data)
            time.sleep(0.1)

    def stop(self):
        print("worker stop")
        self.tracker.stop_tracking()
        self.terminate()


class UICalibrationCircle(QWidget):
    def __init__(self, parent=None):
        super(UICalibrationCircle, self).__init__(parent)

        self.circle = QLabel(self)
        self.circle.resize(30, 30)
        self.circle.setStyleSheet("border: 3px solid blue; border-radius: 40px;")


class UICalibrate(QWidget):
    currentIndex = 0
    # points_to_calibrate = [(0.1, 0.1), (0.1, 0.5), (0.1, 0.9), (0.5, 0.1), (0.5, 0.5), (0.5, 0.9), (0.9, 0.1),
    #                        (0.9, 0.5), (0.9, 0.9)]
    points_to_calibrate = [(0.1, 0.1), (0.1, 0.9), (0.5, 0.5), (0.9, 0.1), (0.9, 0.9)]
    currentPoint = None

    # calibration = None

    def __init__(self, parent=None):
        super(UICalibrate, self).__init__(parent)

        self.vbox = QVBoxLayout()
        self.vbox.setAlignment(Qt.AlignCenter)
        self.setLayout(self.vbox)

        self.currentPoint = UICalibrationCircle(self)
        self.currentPoint.hide()

        self.worker = WorkerThread()
        self.worker.start()

        print("done init")

    def moveCalibrationPoint(self):
        if self.currentIndex > 0:
            currentPoint = self.points_to_calibrate[self.currentIndex - 1]
            if self.worker.calibration.collect_data(currentPoint[0], currentPoint[1]) != tr.CALIBRATION_STATUS_SUCCESS:
                print("not ok")
            else:
                print("ok")

        if self.currentIndex >= len(self.points_to_calibrate):
            self.timer.stop()
            print("stop")
            print("Computing and applying calibration.")

            calibration_result = self.worker.calibration.compute_and_apply()

            print("Compute and apply returned {0} and collected at {1} points.".format(calibration_result.status, len(
                calibration_result.calibration_points)))

            self.worker.calibration.leave_calibration_mode()
            self.worker.stop()
            return

        correctPoint = self.points_to_calibrate[self.currentIndex]
        self.currentPoint.move(int(widthScreen * correctPoint[0]), int(heightScreen * correctPoint[1]))
        self.currentPoint.show()
        self.currentIndex = int(self.currentIndex) + 1


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # self.setFixedSize(widthScreen, heightScreen)
        # self.showMaximized()
        self.showFullScreen()
        self.startUICalibration()

    def startUICalibration(self):
        self.Calibrate = UICalibrate(self)
        self.setWindowTitle("Calibrate")
        self.setCentralWidget(self.Calibrate)
        # self.Calibrate.backBtn.clicked.connect(self.startUIMenu)

        self.show()

        self.Calibrate.timer = QTimer()
        self.Calibrate.timer.setInterval(2500)
        self.Calibrate.timer.timeout.connect(self.Calibrate.moveCalibrationPoint)

        self.Calibrate.timer.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())

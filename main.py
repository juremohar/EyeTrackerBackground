from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import time

from EyeTrackerService import EyeTracker
from FileSave import FileSave

print("start of program")


class WorkerThread(QThread):
    updateProgress = pyqtSignal(int)

    def run(self):
        self.tracker = EyeTracker()
        self.tracker.start_tracking()

        self.file_save = FileSave()

        while True:
            data = self.tracker.get_data()
            self.file_save.addToDataCollection(data)
            time.sleep(0.1)

        # for x in range(1, 100):
        #     # print(x)
        #     time.sleep(0.1)
        #     # data = self.tracker.get_avg_pos()
        #     data = self.tracker.get_data()
        #     self.file_save.addToDataCollection(data)
            # self.updateProgress.emit(x)

    def stop(self):
        print("worker stop")

        self.file_save.saveDataToFile(time.strftime('%d_%m_%Y_%H_%M_%S'))
        self.tracker.stop_tracking()
        self.terminate()


class WindowsTrayUi(QMainWindow):
    def __init__(self, parent=None):
        super(WindowsTrayUi, self).__init__(parent)
        self.icon = QIcon("icon.png")

        # Adding item on the menu bar
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.icon)
        self.tray.setVisible(True)

        self.menu = QMenu()
        self.option_start_tracking = QAction("Start tracking")
        self.option_start_tracking.triggered.connect(self.start_tracking)

        self.option_stop_tracking = QAction("Stop tracking")
        self.option_stop_tracking.triggered.connect(self.stop_tracking)

        self.option_quit = QAction("Quit")
        self.option_quit.triggered.connect(app.quit)

        self.menu.addAction(self.option_start_tracking)
        self.menu.addAction(self.option_stop_tracking)
        self.menu.addAction(self.option_quit)

        self.tray.setContextMenu(self.menu)

        self.worker = WorkerThread()

        print("done init")

    def start_tracking(self):
        print("start tracking")
        self.worker.start()

    def stop_tracking(self):

        file_saver = FileSave()

        print("stop tracking")
        self.worker.stop()


if __name__ == '__main__':
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)
    tray = WindowsTrayUi()
    app.exec_()

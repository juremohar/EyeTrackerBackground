import os
import sys
from PyQt5.QtCore import QThread
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import time

from EyeTrackerService import EyeTracker
from FileSave import FileSave

from RpycServer import RpycServer
from rpyc.utils.server import ThreadedServer

print("start of program")


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class WorkerThread(QThread):
    def run(self):
        self.tracker = EyeTracker()
        self.tracker.start_tracking()

        self.file_save = FileSave()

        while True:
            data = self.tracker.get_data()
            self.file_save.addToDataCollection(data)
            time.sleep(0.1)

    def stop(self, location):
        print("worker stop")

        if location is None:
            location = time.strftime('%d_%m_%Y_%H_%M_%S') + ".json"

        self.file_save.saveDataToFile(location)
        self.tracker.stop_tracking()
        self.terminate()


class RpycServerWorker(QThread):
    def run(self):
        t = ThreadedServer(RpycServer(tray), port=33333)
        t.start()

    def stop(self):
        self.terminate()


class WindowsTrayUi(QMainWindow):
    def __init__(self, parent=None):
        super(WindowsTrayUi, self).__init__(parent)
        self.icon = QIcon(resource_path("icon.png"))

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
        self.option_quit.triggered.connect(self.application_quit)

        self.menu.addAction(self.option_start_tracking)
        self.menu.addAction(self.option_stop_tracking)
        self.menu.addAction(self.option_quit)

        self.tray.setContextMenu(self.menu)

        self.worker = WorkerThread()

        print("done init")

    def start_tracking(self):
        if not self.worker.isRunning():
            self.worker.start()
        else:
            self.worker.tracker.start_tracking()

    def stop_tracking(self, location=None):
        self.worker.stop(location)

    def application_quit(self):
        rpyc_worker.stop()
        app.quit()


if __name__ == '__main__':
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)
    tray = WindowsTrayUi()

    rpyc_worker = RpycServerWorker()
    rpyc_worker.start()

    app.exec_()

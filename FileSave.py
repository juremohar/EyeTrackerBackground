import os
import json
import time


class FileSave:
    folder_path = None
    data_collection = []

    def __init__(self):
        if self.folder_path is None:
            self.folder_path = os.path.join(os.environ['APPDATA'], 'EyeTracker')

        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)

    def addToDataCollection(self, data):
        self.data_collection.append(data)

    def saveDataToFile(self, location=None):

        if not location:
            location = os.path.join(self.folder_path, time.strftime('%d_%m_%Y_%H_%M_%S') + ".json")

        with open(location, 'w') as fp:
            json.dump(self.data_collection, fp)

        print("saved - " + str(len(self.data_collection)))

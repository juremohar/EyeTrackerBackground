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

    def saveDataToFile(self, file_name):
        path = os.path.join(self.folder_path, file_name + ".json")

        with open(path, 'w') as fp:
            json.dump(self.data_collection, fp)

        print("saved - " + str(len(self.data_collection)))

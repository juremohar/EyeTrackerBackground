

import json
import os

newData = []

with open('11_05_2021_19_01_07.json') as f:
    data = json.load(f)
    for line in data:
        if isinstance(line, list):
            continue

        if line['right_gaze_origin_validity'] is 0 or line["left_gaze_origin_validity"] is 0:
            continue

        # 11.5.2021 19:00
        if line['timestamp'] <= 1620752430 or line['timestamp'] > 1620752450:
            continue

        newData.append(line)

    folder_path = os.path.join(os.environ['APPDATA'], 'EyeTracker')

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    path = os.path.join(folder_path, "sorted.json")

    with open(path, 'w') as fp:
        json.dump(newData, fp)





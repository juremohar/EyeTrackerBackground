import json
import os

newData = []

primerStevilka = 1

path = os.path.join("C:\\Users\\PC\\Desktop\\data\\naloga4\\primer" + str(primerStevilka) + "\\primer" + str(primerStevilka) + ".json")

with open(path) as f:
    data = json.load(f)
    for line in data:
        if isinstance(line, list):
            continue

        if line is None:
            continue

        if line['device_time_stamp'] is None:
            continue

        if line['device_time_stamp'] >= 8028187524:
            newData.append(line)

    savePath = os.path.join("C:\\Users\\PC\\Desktop\\data\\naloga4\\primer" + str(primerStevilka) + "\\primer" + str(primerStevilka) + "_fixed.json")
    with open(savePath, 'w') as fp:
        json.dump(newData, fp)


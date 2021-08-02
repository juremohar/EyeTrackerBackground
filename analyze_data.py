import json
import numpy as np

location = "C://diplomska_kalibracija_rezultati//result_15_06_2021_19_21_20.json"
with open(location, 'r') as fp:
    data = json.load(fp)

    totalX = 0
    totalY = 0

    for point in data:
        left = point["left"]
        right = point["right"]
        xs = (left[0], right[0])
        ys = (left[1], right[1])

        # if all of the axes have data from at least one eye
        if not (np.isnan(xs)).all() or not (np.isnan(ys)).all():
            avgEyePos = (np.nanmean(xs), np.nanmean(ys))
        else:
            avgEyePos = (0, 0, 0)

        diff = (np.abs(point["pos"][0] - avgEyePos[0]), np.abs(point["pos"][1] - avgEyePos[1]))
        totalX = totalX + float(diff[0])
        totalY = totalY + float(diff[1])
        print(diff)

    print(totalX, totalY)


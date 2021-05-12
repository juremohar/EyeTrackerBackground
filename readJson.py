import json

# Opening JSON file
import numpy as np

f = open('08_05_2021_12_25_00.json', )

# returns JSON object as
# a dictionary
data = json.load(f)

# Iterating through the json
# list

x = 1920
y = 1080

for row in data:
    lOriginXYZ = row['left_gaze_point_on_display_area']
    rOriginXYZ = row['right_gaze_point_on_display_area']

    # create arrays with positions of both eyes on x, y, and z axes
    xs = (lOriginXYZ[0], rOriginXYZ[0])
    ys = (lOriginXYZ[1], rOriginXYZ[1])

    # if all of the axes have data from at least one eye
    if not (np.isnan(xs)).all() or not (np.isnan(ys)).all():
        avgEyePos = (np.nanmean(xs), np.nanmean(ys))
    else:
        avgEyePos = (0, 0, 0)


    xR = avgEyePos[0] * x
    yR = avgEyePos[1] * y
    print(xR, " - ", yR)

# Closing file
f.close()
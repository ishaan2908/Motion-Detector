import cv2
import time
import pandas as pd
from datetime import datetime

firstFrame = None
statusList = [None, None]
time_list = []
DF = pd.DataFrame(columns = ["Start Time", "End Time"])

video = cv2.VideoCapture(0)

while True:
    check, frame = video.read()
    stat = 0
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if firstFrame is None:
        firstFrame = gray
        continue

    deltaFrame = cv2.absdiff(firstFrame, gray)
    thresholdFrame = cv2.threshold(deltaFrame, 30, 255, cv2.THRESH_BINARY)[1]
    thresholdFrame = cv2.dilate(thresholdFrame, None, iterations = 1)

    contours, hierachy = cv2.findContours(thresholdFrame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 10000:
            continue
        stat = 1

        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
    statusList.append(stat)

    statusList = statusList[-2:]


    if statusList[-1] == 1 and statusList[-2] == 0:
        time_list.append(datetime.now())
    if statusList[-1] == 0 and statusList[-2] == 1:
        time_list.append(datetime.now())


    cv2.imshow("Gray Frame", gray)
    # cv2.imshow("Delta Frame", deltaFrame)
    cv2.imshow("Threshold Frame", thresholdFrame)
    cv2.imshow("Color Frame", frame)

    if cv2.waitKey(1) == ord('q'):
        if stat == 1:
            time_list.append(datetime.now())
        break

print(statusList)
print(time_list)

for i in range(0, len(time_list), 2):
    DF = DF.append({"Start Time" : time_list[i], "End Time" : time_list[i + 1]}, ignore_index = True)

DF.to_csv("Time Data.csv")

video.release()
cv2.destroyAllWindows
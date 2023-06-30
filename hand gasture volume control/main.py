import cv2 as cv
import math
import numpy as np
import time
import hand_tracking_module as htm
import pycaw
import volumeController
import audioControl as AC

wCam, hCam = 688, 488

def calculateDist(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    distance = math.sqrt(math.pow(x1-x2, 2) + math.pow(y1-y2, 2))
    return distance


cam = cv.VideoCapture(0)
cam.set(3, wCam)
cam.set(4, hCam)

cTime = 0
pTime = 0
detector = htm.HandTracker(minDetCon=0.7)
# controller = volumeController.AudioController('chrome.exe')
# controller.set_volume(ratio)
audioController = AC.AudioControl()

while 1 :
    success, frame = cam.read()
    frame = cv.flip(frame, 1)

    detector.findHands(frame, False)
    HandPositions = detector.findPosition(frame)
    if len(HandPositions):
        thumb = (HandPositions[4][1] , HandPositions[4][2])
        finger1 = (HandPositions[8][1] , HandPositions[8][2])
        finger4 = (HandPositions[20][1] , HandPositions[20][2])
        base = (HandPositions[0][1] , HandPositions[0][2])

        handToThumb = calculateDist(thumb, base)
        thumbToFinger = calculateDist(thumb, finger1)
        fingToFing = calculateDist(thumb, finger4)

        if (fingToFing < 30):
            cv.circle(frame, thumb, 10, (255, 0, 255), -1)
            cv.circle(frame, finger4, 10, (255, 0, 255), -1)
            audioController.mute()
        else :
            ratio = thumbToFinger / handToThumb
            volume = int(100*ratio)
            audioController.setVolume(volume)

            cv.circle(frame, thumb, 10, (255,0,255), -1)
            cv.circle(frame, finger1, 10, (255, 0, 255), -1)
            cv.line(frame, thumb, finger1, (0,0,255), 2)

    cTime = time.time()
    fps = int(1/(cTime - pTime))
    pTime = cTime
    cv.putText(frame, str(fps), (10,40), cv.FONT_HERSHEY_PLAIN, 3, (80,255,0),3 )
    cv.imshow('camera', frame)
    cv.waitKey(1)
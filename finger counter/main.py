import cv2 as cv
import hand_tacking_module as htm
import time
import math

def calDist(base, finger ):
    distance = math.sqrt(math.pow(base[0] - finger[0], 2) + math.pow(base[1] - finger[1], 2))
    return distance

cam = cv.VideoCapture(0)
cam.set(3, 688)
cam.set(4, 488)

detector = htm.HandTracker(minDetCon=0.7)
fingTipIdx = [8, 12, 16, 20]

cTime = 0
pTime =0

while 1:
    success, frame = cam.read()
    frame = cv.flip(frame, 1)
    detector.findHands(frame)
    positions = detector.findPosition(frame)
    if len(positions):
        base = (positions[0][1], positions[0][2])
        thumb = (positions[4][1], positions[4][2])
        midL = (positions[13][1], positions[13][2])
        count =0;
        for fing in fingTipIdx:
            fingerU = (positions[fing][1], positions[fing][2])
            fingerL = (positions[fing-3][1], positions[fing-3][2])
            # print(calDist(base, fingerU, fingerL))
            if(calDist(base, fingerU) > calDist(base, fingerL)):
                count +=1
        if(calDist(thumb, midL) > 50):count+=1

        cv.putText(frame, f'finger count :{count}', (244, 50), cv.FONT_HERSHEY_PLAIN, 3 , (255,0,0), 3)
    else:
        cv.putText(frame, 'place your hand in front of camera', (200, 50), cv.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
    cTime = time.time()
    fps = int(1/(cTime - pTime))
    pTime = cTime
    cv.putText(frame, str(fps), (10,50), cv.FONT_HERSHEY_PLAIN, 3, (80,255,20), 3)
    cv.imshow('camera', frame)
    cv.waitKey(1)
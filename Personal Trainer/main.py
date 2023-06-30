import cv2 as cv
import math
import time
import pose_tracking_module as ptm

def slope(x1, y1, x2, y2): # Line slope given two points:
    dx = x2-x1
    dy = y2-y1
    if dx!=0:return dy/dx
    else: return 90.0


def calAngle(pt1, pt2, pt3):
    lineA = (pt1, pt2)
    lineB = (pt2, pt3)

    slope1 = slope(lineA[0][0], lineA[0][1], lineA[1][0], lineA[1][1])
    slope2 = slope(lineB[0][0], lineB[0][1], lineB[1][0], lineB[1][1])

    angle = math.degrees(math.atan((slope2 - slope1) / (1 + (slope2 * slope1))))
    if angle<0: return angle+180
    if angle > 360:return angle -360
    return angle


cam = cv.VideoCapture('dumbbellCurls.mp4')
cam.set(3, 688)
cam.set(4, 488)

detector = ptm.PoseTracker(minDetConf=0.7)
cTime =0
pTime =0
leftFacing = True
angle1 = 0
angle2 = 0

count =0.0
goingUpward = True
goingDownward = False
while 1 :
    success, frame = cam.read()
    frame = cv.flip(frame, 1)
    detector.findPose(frame)
    positions = detector.findPositions(frame)

    lShoulder = positions[11][1], positions[11][2]
    lElbow = positions[13][1], positions[13][2]
    lHand = positions[15][1], positions[15][2]

    lAnkle = positions[27][1], positions[27][2]
    rAnkle = positions[28][1], positions[28][2]

    rShoulder = positions[12][1], positions[12][2]
    rElbow = positions[14][1], positions[14][2]
    rHand = positions[16][1], positions[16][2]

    if lAnkle[1] > rAnkle[1]:leftFacing = False
    angle1 = calAngle(lShoulder, lElbow, lHand) - 10
    angle2 = calAngle(rShoulder, rElbow, rHand)

    if not leftFacing:
        angle1 = 180 - angle1 + 10
        angle2 = 180 - angle2 - 10

    if angle1<60 and angle2 <60 and goingUpward:
        count+= 0.5
        goingUpward = False
        goingDownward = True
    if angle1 > 150 and angle2 >150 and goingDownward:
        count+= 0.5
        goingDownward = False
        goingUpward = True
    print(angle1, angle2)

    cTime = time.time()
    fps = int(1/(cTime - pTime))
    pTime = cTime
    cv.putText(frame, f'FPS :{fps}', (10,350), cv.FONT_HERSHEY_PLAIN, 3, (80,255,20), 3)
    cv.putText(frame, f'Total correct curls : {int(count)}', (10, 30), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

    cv.imshow('video', frame)
    cv.waitKey(1)

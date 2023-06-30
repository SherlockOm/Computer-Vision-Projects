import mediapipe as mp
import cv2 as cv
import time


class PoseTracker():
    def __init__(self, mode = False, cmplx=1, smoothLmks=True, enSeg = False,
                 smoothSeg=True, minDetConf=0.5, minTrackConf=0.5):
        self.image_mode = mode
        self.complexity = cmplx
        self.smooth_lms = smoothLmks
        self.enable_segment = enSeg
        self.smooth_segment = smoothSeg
        self.min_det_conf = minDetConf
        self.min_track_conf = minTrackConf

        self.mpPose = mp.solutions.pose
        self.mpDraw = mp.solutions.drawing_utils
        self.pose = self.mpPose.Pose(self.image_mode, self.complexity, self.smooth_lms, self.enable_segment, self.smooth_segment,
                           self.min_det_conf, self.min_track_conf)

    def findPose(self, img, draw=True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.result = self.pose.process(img)
        if (self.result.pose_landmarks and draw):
            self.mpDraw.draw_landmarks(img, self.result.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

    def findPositions(self, img, bodyNo=0, draw=True):
        lmsList = []
        # print(len(self.result.pose_landmarks.landmark))
        if (self.result.pose_landmarks):
            myBody = self.result.pose_landmarks

            h, w, c = img.shape
            for id, lm in enumerate(myBody.landmark):
                cx, cy = int(lm.x*w) , int(lm.y*h)
                lmsList.append([id, cx, cy])

        return lmsList


def main():
    cam = cv.VideoCapture('resources/dance.mp4')

    detector = PoseTracker()
    cTime = 0
    pTime = 0
    while 1:
        success, frame = cam.read()
        h, w, c = frame.shape
        w = int(w/3)
        h = int(h/3)
        frame = cv.resize(frame, (w, h), interpolation=cv.INTER_CUBIC)
        detector.findPose(frame)
        positions = detector.findPositions(frame, 0)
        print(positions)
        if len(positions):
            cv.circle(frame, (positions[0][1], positions[0][2]), 5, (0,255,0), -1)

        cTime = time.time()
        fps = int(1 / (cTime - pTime))
        pTime = cTime
        cv.putText(frame, str(fps), (10, 70), cv.FONT_HERSHEY_PLAIN, 3, (20, 255, 20), 3)

        cv.imshow('camera', frame)
        cv.waitKey(1)


if __name__=='__main__':
    main()
import cv2 as cv
import mediapipe as mp
import numpy as np

mpSelfie = mp.solutions.selfie_segmentation
segment = mpSelfie.SelfieSegmentation(model_selection=0)

vid = cv.VideoCapture(0)

while 1:
    success, img = vid.read()
    img = cv.resize(img , (640 , 360))

    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    result = segment.process(imgRGB)
    mask = result.segmentation_mask > 0.5
    mask = mask.astype(np.uint8)
    mask3 = np.dstack((mask, mask, mask))

    bgImg = cv.GaussianBlur(img, (19, 19), 0)
    bgImg = cv.cvtColor(bgImg, cv.COLOR_BGR2GRAY)
    bgImg = np.dstack((bgImg, bgImg, bgImg))

    output = np.where(mask3, img, bgImg)
    cv.imshow('output', output)
    cv.waitKey(1)

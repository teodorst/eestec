import cv2
import numpy as np
import math

cap = cv2.VideoCapture(0)

while(cap.isOpened()):
    ret, img = cap.read()
    cv2.rectangle(img,(300,300),(100,100),(0,255,0),0)
    crop_img = img
    grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    value = (35, 35)
    
    blurred = cv2.GaussianBlur(grey, value, 0)
    
    _, thresh1 = cv2.threshold(blurred, 127, 255,
                               cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    

    cv2.imshow('Thresholded', thresh1)

    k = cv2.waitKey(10)
    if k == 27:
        break
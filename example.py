import cv2
import numpy as np
import math
from communicator import Communicator

cap = cv2.VideoCapture(0)

lower_range = np.array([14, 135, 139], dtype=np.uint8)
upper_range = np.array([30, 255, 255], dtype=np.uint8)

#lower_range = np.array([199, 161, 149], dtype=np.uint8)
#upper_range = np.array([219, 181, 169], dtype=np.uint8)

com = Communicator("localhost", 10000)


def get_center(cnt):
    M = cv2.moments(cnt)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    return (cx, cy)

def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

def find_squares(img):
    squares = []
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gaussian = cv2.GaussianBlur(gray, (5, 5), 0)
    temp,bin = cv2.threshold(gaussian, 80, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(bin, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours( gray, contours, -1, (0, 255, 0), 3 )
    max_area = 0

    for cnt in contours:
        cnt_len = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt,0.01 * cv2.arcLength(cnt,True),True)
        cnt = cv2.approxPolyDP(cnt, 0.02 * cnt_len, True)
        area = cv2.contourArea(cnt)
        if area > 500 and area > max_area and len(cnt) >= 2:
            max_area = area
            (cx, cy) = get_center(cnt)
            S = 1 if area > 5000 else 0
            tosend = [640 - cx, cy, S]
            com.send_message(tosend)
            #print("trying to send" + str(tosend))
            squares.append(cnt)
    return squares

while(cap.isOpened()):
    ret, img = cap.read()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(img, lower_range, upper_range)
    img = cv2.bitwise_and(img, img, mask = mask)

    squares = find_squares(img)
    #print "Find %d squres" % len(squares)
    cv2.drawContours( mask, squares, -1, (0, 255, 0), 3 )
    cv2.imshow('squares', img)
    k = cv2.waitKey(10)
    if k == 27:
        break

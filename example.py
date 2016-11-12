import cv2
import numpy as np
import math
from communicator import Communicator

cap = cv2.VideoCapture(0)
red = ([170, 160, 60], [180, 255, 255])
lower = np.array([0, 70, 0])
upper = np.array([10, 255, 255])
lower_red_1 = np.array([0, 70, 50])
upper_red_1 = np.array([10,255,255])
lower_red_2 = np.array([170,70,50])
upper_red_2 = np.array([180,255,255])
# red
lower_range = np.array([140, 100, 100], dtype=np.uint8)
upper_range = np.array([200, 255, 255], dtype=np.uint8)
# yellow
#lower_range = np.array([20, 20, 20], dtype=np.uint8)
#upper_range = np.array([35, 255, 255], dtype=np.uint8)

com = Communicator("localhost", 10000)


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
    x = 0
    y = 0
    for cnt in contours:
        cnt_len = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        cnt = cv2.approxPolyDP(cnt, 0.02 * cnt_len, True)
        area = cv2.contourArea(cnt)
        if area > 100 and area > max_area and len(cnt) >= 4:
            max_area = area
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            squares.append(cnt)
            S = 1 if area > 5000 else 0
            com.send_message([cx, cy, S])
            print(str(area))

        #if x != 0 or y != 0:
            #cv2.circle(img,(x,y), int(abs(area / 100)), (0,0,255), -1)
            #print("x=" + str(x) + " y=" + str(y))
    return squares


while(cap.isOpened()):
    ret, img = cap.read()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(img, lower_red_1, upper_red_1)
    mask2 = cv2.inRange(img, lower_red_2, upper_red_2)
    mask3 = cv2.inRange(img, lower, upper)
    mask4 = cv2.inRange(img, lower_range, upper_range)
    mask = mask1 + mask2 + mask3 + mask4
    img = cv2.bitwise_and(img, img, mask = mask)

    squares = find_squares(img)
    print "Find %d squres" % len(squares)
    cv2.drawContours( mask, squares, -1, (0, 255, 0), 3 )
    cv2.imshow('squares', mask)

    #cv2.imshow('circle', img)

    
    #cv2.imshow('Img', mask4)
    k = cv2.waitKey(10)
    if k == 27:
        break

import cv2
import numpy as np
import math
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

def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

def find_squares(img):
    squares = []
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("gray", gray)

    gaussian = cv2.GaussianBlur(gray, (5, 5), 0)

    temp,bin = cv2.threshold(gaussian, 80, 255, cv2.THRESH_BINARY)
    # cv2.imshow("bin", bin)

    contours, hierarchy = cv2.findContours(bin, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours( gray, contours, -1, (0, 255, 0), 3 )

    #cv2.imshow('contours', gray)
    for cnt in contours:
        cnt_len = cv2.arcLength(cnt, True)
        cnt = cv2.approxPolyDP(cnt, 0.02 * cnt_len, True)

        if cv2.contourArea(cnt) > 70 and len(cnt) >= 4:
            
            squares.append(cnt)
    return squares


while(cap.isOpened()):
    ret, img = cap.read()
    # cv2.rectangle(img,(300,300),(100,100),(0,255,0),0)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(img, lower_red_1, upper_red_1)
    mask2 = cv2.inRange(img, lower_red_2, upper_red_2)
    mask3 = cv2.inRange(img, lower, upper)
    mask4 = cv2.inRange(img, lower_range, upper_range)
    mask = mask1 + mask2
    img = cv2.bitwise_and(img, img, mask = mask1)


    squares = find_squares(img)
    print "Find %d squres" % len(squares)
    cv2.drawContours( img, squares, -1, (0, 255, 0), 3 )
    cv2.imshow('squares', img)

    #cv2.imshow('Img', mask4)
    k = cv2.waitKey(10)
    if k == 27:
        break

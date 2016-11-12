import cv2
import numpy as np
import math
from communicator import Communicator


cap = cv2.VideoCapture(0)
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
    for cnt in contours:
        cnt_len = cv2.arcLength(cnt, True)
        cnt = cv2.approxPolyDP(cnt, 0.02 * cnt_len, True)
        area = cv2.contourArea(cnt)

        if area > 500 and len(cnt) >= 4:
            squares.append(cnt)
            if area > 5000 and area > max_area:
                max_area = area


    if len(squares) > 1:
        squares = [squares[0]]
    return (squares, max_area > 0)



# def find_result_shape(shapes):
# 	x_min, y_min = (640, 480)
# 	x_max, y_max = (0, 0)
# 	for shape in shapes:
# 		# coords = np.nditer(shape, flags=['external_loop'])
# 		for x in range(0, len(coords), 2):
			
# 			print x


# yellow
lower_range = np.array([14, 135, 139], dtype=np.uint8)
upper_range = np.array([30, 255, 255], dtype=np.uint8)



while(cap.isOpened()):
    ret, img = cap.read()
    # cv2.rectangle(img,(300,300),(100,100),(0,255,0),0)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(img, lower_range, upper_range)
    img = cv2.bitwise_and(img, img, mask = mask)
    sq, click = find_squares(img)
    if sq:
        M = cv2.moments(sq[0])
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        if click:
            com.send_message([cx, cy, 1])
        else:
            com.send_message([cx, cy, 1])

        cv2.drawContours( img, sq, -1, (0, 255, 0), 3 )
    
        print 'Clicked ? %r' % click
    # print sq
    

    cv2.imshow('Img', img)
    

    k = cv2.waitKey(10)
    if k == 27:
        break

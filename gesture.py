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
# lower_range = np.array([169, 100, 100], dtype=np.uint8)
# upper_range = np.array([189, 255, 255], dtype=np.uint8)


# yellow
lower_range = np.array([14, 135, 139], dtype=np.uint8)
upper_range = np.array([30, 255, 255], dtype=np.uint8)


while(cap.isOpened()):
    ret, img = cap.read()
<<<<<<< HEAD
    # cv2.rectangle(img,(300,300),(100,100),(0,255,0),0)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    mask1 = cv2.inRange(img, lower_red_1, upper_red_1)
    mask2 = cv2.inRange(img, lower_red_2, upper_red_2)
    mask3 = cv2.inRange(img, lower, upper)
    mask4 = cv2.inRange(img, lower_range, upper_range)

    mask = mask1 + mask2

    img = cv2.bitwise_and(img, img, mask = mask1)
    
    # with open('img.txt', 'w') as f:
    # 	f.write(img)

    # with open('mask.txt', 'w') as f:
    # 	f.write(mask)
    
    # break;
    
    cv2.imshow('Img', mask4)

    k = cv2.waitKey(10)
    if k == 27:
        break


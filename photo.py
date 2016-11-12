import cv2
import numpy as np
import math
from communicator import Communicator
import scipy.misc

cap = cv2.VideoCapture(0)
ret, img = cap.read()

cv2.imshow('img', img)

scipy.misc.imsave("output.jpg", img)

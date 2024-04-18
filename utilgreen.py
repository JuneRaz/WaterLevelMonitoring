import numpy as np
import cv2

def get_limits2(color):
    c = np.uint8([[color]])  # BGR values
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

    hue = hsvC[0][0][0]  # Get the hue value

    # Green hue range
    lowerLimit = np.array([hue - 20, 100, 100], dtype=np.uint8)
    upperLimit = np.array([hue + 20, 255, 255], dtype=np.uint8)

    return lowerLimit, upperLimit

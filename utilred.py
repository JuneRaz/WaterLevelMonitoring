import numpy as np
import cv2

def get_limits(color):
    c = np.uint8([[color]])  # BGR values
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

    hue = hsvC[0][0][0]  # Get the hue value

    # Red hue range
    if hue >= 165 or hue <= 15:  # Handle red hue wrap-around
        lowerLimit1 = np.array([0, 100, 100], dtype=np.uint8)
        upperLimit1 = np.array([15, 255, 255], dtype=np.uint8)
        lowerLimit2 = np.array([165, 100, 100], dtype=np.uint8)
        upperLimit2 = np.array([180, 255, 255], dtype=np.uint8)
        return lowerLimit1, upperLimit1, lowerLimit2, upperLimit2
    else:
        lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)
        return lowerLimit, upperLimit

# Your main code goes here

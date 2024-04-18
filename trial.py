import cv2
import os, shutil
from utilred import get_limits
from utilYellow import get_limits1
from utilgreen import get_limits2

red = [0, 0, 255]  # red in BGR colorspace
yellow = [0, 255, 255]  # yellow in BGR colorspace
green = [0, 255, 0]  # green in BGR colorspace

# cap = cv2.VideoCapture("../trial1.mp4")
ip = input("Please insert the ip of your camera >>")
user = input("Please input the username >>")
password = input("Please input the password >>")

source = 'rtsp://'+user+':'+password+'@'+ip+'/cam/realmonitor?channel=1&subtype=0'
#source = 'rtsp://admin:Admin12345@192.168.1.65/cam/realmonitor?channel=1&subtype=0'


cap = cv2.VideoCapture(source)
# cap.set(3, 1280)  # Set width
# cap.set(4, 720)  # Set height

while True:
    ret, frame = cap.read()

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Get the lower and upper limits for red color
    lower_red1, upper_red1, lower_red2, upper_red2 = get_limits(red)

    # Threshold the HSV image to get only red colors
    mask1 = cv2.inRange(hsvImage, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsvImage, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(mask1, mask2)

    # Get the bounding box of the red color area
    contours_red, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Yellow detection
    yellow_lower, yellow_upper = get_limits1(yellow)
    yellow_mask = cv2.inRange(hsvImage, yellow_lower, yellow_upper)

    # Get the bounding box of the yellow color area
    contours_yellow, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Green detection
    green_lower, green_upper = get_limits2(green)
    green_mask = cv2.inRange(hsvImage, green_lower, green_upper)

    # Get the bounding box of the green color area
    contours_green, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw rectangles for detected objects
    for cnt in contours_red:
        x, y, w, h = cv2.boundingRect(cnt)
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 5)

    for cnt in contours_yellow:
        x, y, w, h = cv2.boundingRect(cnt)
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 5)

    for cnt in contours_green:
        x, y, w, h = cv2.boundingRect(cnt)
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 5)

    # Draw gauge
    gauge_color = (0, 0, 0)  # Default: Black (All colors detected)
    if not contours_red and not contours_yellow and not contours_yellow:
        gauge_color = (0, 0, 255)  # Red: Danger (No red detected)
        cv2.putText(frame, "Danger", (85, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    elif not contours_yellow and not contours_green:
        gauge_color = (0, 255, 255)  # Yellow: Warning (No yellow detected)
        cv2.putText(frame, "Warning", (85, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
    elif not contours_green:
        gauge_color = (0, 255, 0)  # Green: Safe (No green detected)
        cv2.putText(frame, "Normal", (85, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.putText(frame, "Gauge", (25, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.circle(frame, (50, 100), 30, gauge_color, -1)  # Draw circle indicator


    cv2.imshow('frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
import numpy as np
import cv2

cap = cv2.VideoCapture(0)

ret, last_frame = cap.read()

if last_frame is None:
    exit()

while(cap.isOpened()):
    ret, frame = cap.read()

    if frame is None:
        break

    a = cv2.absdiff(last_frame, frame)

    cv2.imshow('frame', frame)
    cv2.imshow('a', a)

    if cv2.waitKey(33) >= 0:
        break

    last_frame = frame

cap.release()
cv2.destroyAllWindows()
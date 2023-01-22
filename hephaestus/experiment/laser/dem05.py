import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while (1):

    # Take each frame
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 0, 255])
    upper_red = np.array([255, 255, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)

    moments = cv2.moments(hsv[:, :, 2])
    x = int(moments['m10'] / moments['m00'])
    y = int(moments['m01'] / moments['m00'])
    print(x, y)

    cv2.circle(frame, (x, y), 20, (0, 255, 0), 3)
    cv2.circle(mask, (x, y), 20, (0, 255, 0), 3)

    cv2.imshow('mask', mask)
    cv2.imshow('Track Laser', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

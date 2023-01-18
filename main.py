import cv2
import numpy as np
import mss

import win32api
import win32con
import ait

path = '####' # cascade path
obj = 'target' # detected obj name (for display)

# cascade values for tweaking
scale = 2 # lower scale = better detection = lower performance
min_neig = 4 # lower minimum neighbour = more detection (might be false detection)

cascade = cv2.CascadeClassifier(path)

while True:
    a = win32api.GetKeyState(0x26)  # up arrow key
    if a < 0:
        break

while True:
    with mss.mss() as sct:
        monitor = {"top":0, "left":0, "width":1920, "height":1080}
        img_array = np.array(sct.grab(monitor))

    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    detection = cascade.detectMultiScale(gray, scale, min_neig)
    
    apx = (detection[0][0] + (detection[0][2] / 2)) - 960
    apy = (detection[0][1] + (detection[0][3] / 2)) - 540
    
    print (apx, apy)

    # display detection (uncomment for window that displays what the AI is predicting with bounding boxes)
    for (x, y, w, h) in detection:
        print(x, y, w, h)
        cv2.rectangle(img_array, (x, y), (x + w, y + h), (0, 255, 0), 5)
        cv2.putText(img_array, obj, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    cv2.imshow('winname', img_array)
    cv2.waitKey(1)

    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(apx), int(apy))
    ait.click()

    a = win32api.GetKeyState(0x28)  # down arrow key
    if a < 0:
        break

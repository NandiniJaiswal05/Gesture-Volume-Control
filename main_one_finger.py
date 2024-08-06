
import cv2
import mediapipe as mp
import numpy as np
import time
import hand_tracking as ht
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL, CoInitialize, CoCreateInstance
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

CoInitialize()

wcam, hcam = 648, 488
cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)
pTime = 0

detector = ht.handDetector()

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()
minvol = volRange[0]
maxvol = volRange[1]

vol = 0
volPar = 0

# Variables for tracking finger motion
prev_angle = None
prev_position = None

def calculate_angle(x1, y1, x2, y2):
    return math.degrees(math.atan2(y2 - y1, x2 - x1))

while cap.isOpened():
    r, frame = cap.read()
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame, draw=False)
    
    if len(lmList) != 0:
        x1, y1 = lmList[8][1], lmList[8][2]  # Index finger tip position

        if prev_position is not None:
            prev_x, prev_y = prev_position
            angle = calculate_angle(prev_x, prev_y, x1, y1)

            if prev_angle is not None:
                delta_angle = angle - prev_angle
                if delta_angle > 0:
                    # Clockwise motion
                    vol = min(vol + 1, maxvol)
                else:
                    # Counterclockwise motion
                    vol = max(vol - 1, minvol)

                volume.SetMasterVolumeLevel(vol, None)
                volPar = np.interp(vol, [minvol, maxvol], [0, 100])

            prev_angle = angle
        prev_position = (x1, y1)

        # Visualization
        cv2.circle(frame, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
        cv2.putText(frame, f'Vol: {int(volPar)}%', (52, 98), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
        cv2.rectangle(frame, (40, 30), (190, 110), (0, 255, 0), 2)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(frame, f'FPS: {int(fps)}', (48, 58), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break
    cv2.imshow('volume_gesture_control', frame)
cap.release()
cv2.destroyAllWindows()

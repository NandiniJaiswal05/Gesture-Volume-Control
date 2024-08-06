import cv2, mediapipe as mp, numpy as np,time
import hand_tracking as ht
import math 
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL,CoInitialize, CoCreateInstance
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from facemesh import FaceMeshDetector

CoInitialize

wcam,wcam=648,488
cap= cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,wcam)
pTime=0

detector = ht.handDetector()

mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=3)
drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=1)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange=volume.GetVolumeRange()

minvol = volRange[0]
maxvol = volRange[1]
vol = 0
#volBar=0
volPar=0

while cap.isOpened:
    r,frame=cap.read()
    frame=detector.findHands(frame)
    lmList=detector.findPosition(frame, draw=False)
    if len(lmList) != 0:
       #print(lmList[4],lmList[8])

       x1,y1 = lmList[4][1], lmList[4][2]
       x2,y2 = lmList[8][1], lmList[8][2]
       cx,cy=(x1+x2)//2,(y1+y2)//2

       cv2.circle(frame,(x1,y1),10, (255,0,0),cv2.FILLED)
       cv2.circle(frame,(x2,y2),10, (255,0,0),cv2.FILLED)
       cv2.line(frame, (x1,y1),(x2,y2),(255,0,255),3)
       cv2.circle(frame,(cx,cy),10, (255,0,0),cv2.FILLED)

       lenght=math.hypot(x2-x1,y2-y1)
       #print(lenght)
       
       vol=np.interp(lenght,[5,180],[minvol,maxvol])
       #volBar=np.interp(lenght,[5,110],[380,110])
       volPar=np.interp(lenght, [5,180],[0,100])

       print(vol)
       volume.SetMasterVolumeLevel(vol, None)

       if lenght < 30 :
           cv2.circle(frame, (cx,cy),10, (0,255,0), cv2.FILLED)

    #cv2.rectangle(frame, (8,115), (50,380), (0,255,0), 2)
    #cv2.rectangle(frame, (8,int(vol)), (50,380), (0,255,0), cv2.FILLED)
    cv2.putText(frame,f'Vol:{int(volPar)}%',(52,98),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),3)
    cv2.rectangle(frame, (40,30),(190,110),(0,255,0),2)

    f_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = faceMesh.process(f_rgb)
    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            mpDraw.draw_landmarks(frame, faceLms, mpFaceMesh.FACEMESH_CONTOURS, drawSpec, drawSpec)
            for id, lm in enumerate(faceLms.landmark):
                fh, fw, fc = frame.shape
                x, y = int(lm.x * fw), int(lm.y * fh)

    cTime=time.time()
    fps =1/(cTime-pTime)
    pTime=cTime


    cv2.putText(frame,f'FPS:{int(fps)}',(48,58),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),3)



    if cv2.waitKey(1) & 0xff == ord('q') :
        break
    cv2.imshow('volume_gesture_control',frame)

cap.release()
cv2.destroyAllWindows()    
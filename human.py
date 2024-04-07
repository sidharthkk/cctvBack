import cv2
import pandas as pd
from ultralytics import YOLO
import cvzone
import numpy as np
import pygame
from tracker import *

model = YOLO('yolov8s.pt')
alarm_flag=False

def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        point = [x, y]
        print(point)


cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)
cap = cv2.VideoCapture("testvideo/rob.mp4")

my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")
# print(class_list)

count = 0
tracker = Tracker()
area1 =[(477,188),(433,346),(554,352),(586,197)]
while True:
    ret, frame = cap.read()

    if not ret:
        break

    count += 1
    if count % 3 != 0:
        continue

    frame = cv2.resize(frame, (1020, 500))
    results = model.predict(frame)
    a = results[0].boxes.data
    px = pd.DataFrame(a).astype("float")
    list=[]
    for index, row in px.iterrows():
        #        print(row)

        x1 = int(row[0])
        y1 = int(row[1])
        x2 = int(row[2])
        y2 = int(row[3])
        d = int(row[5])
        c = class_list[d]
        if 'person' in c:
            list.append([x1,y1,x2,y2])
        box_id=tracker.update(list)
        for box in box_id:
            x3,y3,x4,y4,id=box
            cx=int(x3+x4)//2
            cy=int(y3+y4)//2
            result= cv2.pointPolygonTest(np.array(area1,np.int32),((cx,cy)),False)
            print(result)
            if result>=0:
                cv2.circle(frame,(cx,cy),4,(0,255,0),-1)
                cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 0, 255), 2)
                cvzone.putTextRect(frame, f'{id}', (x3, y3), 1, 1)
                if not alarm_flag:
                    pygame.mixer.init()
                    pygame.mixer.music.load('accident/alarm1.mp3')
                    pygame.mixer.music.play()
                    alarm_flag=True
    cv2.polylines(frame,[np.array(area1,np.int32)],True,(255,0,255),2)
    cv2.imshow("RGB", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
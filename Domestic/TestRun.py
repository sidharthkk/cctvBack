import cv2
import cvzone
import math
import pygame
from ultralytics import YOLO
import pandas as pd
import numpy as np
from tracker import Tracker

# Initialize Pygame mixer
pygame.mixer.init()

# Load YOLO models for fire, weapon, and human detection
fire_model = YOLO('fi.pt')
weapon_model = YOLO('gun.pt')
human_model = YOLO('yolov8s.pt')

# Define class names for fire, weapon, and human detection
classnames_fire = ['fire', 'nofire', 'smoke']
classnames_weapon = ['Handgun', 'Knife', 'Missile', 'Rifle', 'Sword']
classnames_human = ['person']

# Load alarm sound
pygame.mixer.music.load('alarm1.mp3')

# Initialize alarm flags for fire, weapon, and human detection
fire_alarm_flag = False
weapon_alarm_flag = False
human_alarm_flag = False

# Open video capture
cap = cv2.VideoCapture('testfire.mp4')

# Create a tracker for human detection
tracker = Tracker()
area1 = [(477, 188), (433, 346), (554, 352), (586, 197)]

while True:
    # Read frame
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (1000, 500))

    # Fire detection
    result_fire = fire_model(frame, stream=True)
    for info in result_fire:
        boxes = info.boxes
        for box in boxes:
            confidence = box.conf[0]
            confidence = math.ceil(confidence * 100)
            Class = int(box.cls[0])
            if confidence > 70 and classnames_fire[Class] == 'fire':
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 5)
                cvzone.putTextRect(frame, f'{classnames_fire[Class]} {confidence}%', (x1, y1 - 10), scale=1,
                                   thickness=2,
                                   colorR=(0, 0, 255))
                if not fire_alarm_flag:
                    pygame.mixer.music.play()
                    fire_alarm_flag = True

    # Weapon detection
    result_weapon = weapon_model(frame, stream=True)
    for info in result_weapon:
        boxes = info.boxes
        for box in boxes:
            confidence = box.conf[0]
            confidence = math.ceil(confidence * 100)
            Class = int(box.cls[0])
            if confidence > 70 and Class < len(classnames_weapon) and classnames_weapon[Class] in ['Handgun', 'Knife',
                                                                                                   'Missile', 'Rifle',
                                                                                                   'Sword']:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 5)
                cvzone.putTextRect(frame, f'{classnames_weapon[Class]} {confidence}%', (x1, y1 - 10), scale=1,
                                   thickness=2,
                                   colorR=(255, 0, 0))
                if not weapon_alarm_flag:
                    pygame.mixer.music.play()
                    weapon_alarm_flag = True

    # Human detection
    result_human = human_model(frame, stream=True)
    for result in result_human:
        a = result.boxes.data
        px = pd.DataFrame(a).astype("float")
        list = []
        for index, row in px.iterrows():
            x1 = int(row[0])
            y1 = int(row[1])
            x2 = int(row[2])
            y2 = int(row[3])
            d = int(row[5])
            if d < len(classnames_human):
                c = classnames_human[d]
            else:
                c = "Unknown"
            if 'person' in c:
                list.append([x1, y1, x2, y2])
        box_id = tracker.update(list)
        for box in box_id:
            x3, y3, x4, y4, id = box
            cx = int(x3 + x4) // 2
            cy = int(y3 + y4) // 2
            result = cv2.pointPolygonTest(np.array(area1, np.int32), ((cx, cy)), False)
            if result >= 0:
                cv2.circle(frame, (cx, cy), 4, (0, 255, 0), -1)
                cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 0, 255), 2)
                cvzone.putTextRect(frame, f'{id}', (x3, y3), 1, 1)
                if not human_alarm_flag:
                    pygame.mixer.music.play()
                    human_alarm_flag = True

    cv2.polylines(frame, [np.array(area1, np.int32)], True, (255, 0, 255), 2)
    cv2.imshow("RGB", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()

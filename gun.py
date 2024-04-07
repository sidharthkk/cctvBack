from ultralytics import YOLO
import cv2
import cvzone
import math
import pygame

cap = cv2.VideoCapture('Female Hands Raising Holding Armed Gun With Blurred Policewo.mp4')
#cap = cv2.VideoCapture('WeaponTest.mp4')
model = YOLO('gun.pt')

classnames = ['Handgun', 'Knife', 'Missile', 'Rifle', 'Handgun', 'Sword']

alarm_flag = False

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (640, 480))
    result = model(frame, stream=True)

    for info in result:
        boxes = info.boxes
        for box in boxes:
            confidence = box.conf[0]
            confidence = math.ceil(confidence * 100)
            Class = int(box.cls[0])
            if confidence > 70:
                if classnames[Class]  in['Handgun', 'Knife', 'Missile', 'Rifle', 'Sword']:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 5)
                    cvzone.putTextRect(frame, f'{classnames[Class]} {confidence}%', [x1 + 8, y1 + 100], scale=1.5, thickness=2)
                    if not alarm_flag:
                        pygame.mixer.init()
                        pygame.mixer.music.load('accident/alarm1.mp3')
                        pygame.mixer.music.play()
                        alarm_flag = True

    cv2.imshow('frame', frame)
    cv2.waitKey(1)

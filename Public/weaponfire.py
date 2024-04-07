import cv2
import cvzone
import math
import pygame
from ultralytics import YOLO

pygame.mixer.init()

# Load YOLO models once (outside the loop for efficiency)
fire_model = YOLO('fi.pt')  # Assuming GPU acceleration if available
weapon_model = YOLO('gun.pt')

classnames_fire = ['fire', 'nofire', 'smoke']
classnames_weapon = ['Handgun', 'Knife', 'Missile', 'Rifle', 'Sword']

fire_alarm_flag = False
weapon_alarm_flag = False

cap = cv2.VideoCapture('testfire.mp4')

# Reduce resolution (optional, adjust as needed)
width, height = 640, 480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Process frame with some optimizations (consider a balance between speed and accuracy)
    fire_results = fire_model(frame, stream=True)  # Assuming GPU acceleration
    weapon_results = weapon_model(frame, stream=True)  # Assuming GPU acceleration

    # Process fire detections
    for info in fire_results:
        boxes = info.boxes
        for box in boxes:
            confidence = box.conf[0]
            confidence = math.ceil(confidence * 100)
            Class = int(box.cls[0])
            if confidence > 70 and classnames_fire[Class] == 'fire':
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cvzone.putTextRect(frame, f'{classnames_fire[Class]} {confidence}%', (x1, y1 - 10), scale=1, thickness=2,
                                   colorR=(0, 0, 255))
                if not fire_alarm_flag:
                    pygame.mixer.music.load('alarm1.mp3')
                    pygame.mixer.music.play()
                    fire_alarm_flag = True

    # Process weapon detections (consider filtering for specific weapons if needed)
    for info in weapon_results:
        boxes = info.boxes
        for box in boxes:
            confidence = box.conf[0]
            confidence = math.ceil(confidence * 100)
            Class = int(box.cls[0])
            if confidence > 70 and Class < len(classnames_weapon) and classnames_weapon[Class] in ['Handgun',
                                                                                                       'Knife',
                                                                                                       'Missile',
                                                                                                       'Rifle',
                                                                                                       'Sword']:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cvzone.putTextRect(frame, f'{classnames_weapon[Class]} {confidence}%', (x1, y1 - 10), scale=1, thickness=2,
                                   colorR=(255, 0, 0))
                if not weapon_alarm_flag:
                    pygame.mixer.music.load('alarm1.mp3')
                    pygame.mixer.music.play()
                    weapon_alarm_flag = True

    cv2.imshow("Fire and Weapon Detection", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()

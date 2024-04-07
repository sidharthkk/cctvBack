import cv2
import ultralytics as ut  # Assuming ultralytics supports GPU acceleration
import cvzone
import math
import pygame
import pandas as pd

pygame.mixer.init()

# Load YOLO models once (outside the loop for efficiency)
fire_model = ut.YOLO('model-fire.pt')  # Assuming GPU is used if available
accident_model = ut.YOLO('carcrash.pt')

with open("road_classes.txt", "r") as my_file:
    class_list = my_file.read().split("\n")

classnames = ['fire', 'nofire', 'smoke']

fire_alarm_flag = False

cap = cv2.VideoCapture('test-fire.mp4')

# Reduce resolution (optional, adjust as needed)
width, height = 640, 480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Process frame here (fire and accident detection)
    fire_results = fire_model(frame, stream=True)
    for info in fire_results:
        boxes = info.boxes
        for box in boxes:
            confidence = box.conf[0]
            confidence = math.ceil(confidence * 100)
            Class = int(box.cls[0])
            if confidence > 70 and classnames[Class] == 'fire':
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cvzone.putTextRect(frame, f'{classnames[Class]} {confidence}%', (x1, y1 - 10), scale=1, thickness=2,
                                   colorR=(0, 0, 255))
                if not fire_alarm_flag:
                    pygame.mixer.music.load('alarm.mp3')
                    pygame.mixer.music.play()
                    fire_alarm_flag = True
    accident_results = accident_model.predict(frame)
    for boxes in accident_results[0].boxes.data:
        x1, y1, x2, y2, _, class_id = map(int, boxes)
        class_name = class_list[class_id]
        if 'accident' in class_name:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cvzone.putTextRect(frame, f'{class_name}', (x1, y1 - 10), scale=1, thickness=2, colorR=(255, 0, 0))

    cv2.imshow("Fire and Accident Detection", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()

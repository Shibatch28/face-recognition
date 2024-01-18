import cv2
import face_recognition
import numpy as np

cap = cv2.VideoCapture(2)
counter = 0
images = []
ids = []
trainerPath = 'trainer/trainer.yml'

while True:
    ret, img = cap.read()
    if ret and counter < 20:
        cv2.imshow('Camera', img)
        auth = face_recognition.entry(img)
        detected = auth.detect()
        if detected is not None and len(detected) > 0:
            images.append(detected)
            ids.append(counter)
            counter += 1
    
    if counter == 20:
        print(ids)
        auth.register(trainerPath, images, ids)
        counter += 1
        continue

    if ret and counter > 20:
        recognized = face_recognition.authentication(trainerPath).recognize(img)
        cv2.imshow('recognized', recognized)
            
    key = cv2.waitKey(1)
    if key==ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
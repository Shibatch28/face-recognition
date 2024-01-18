import cv2
import face_recognition
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    ret, img = cap.read()
    cv2.imshow('Camera', img)
    auth = face_recognition.entry(img)
    recognized = auth.register()

    cv2.imshow('recognized', recognized)
    key = cv2.waitKey(1)
    if key==ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
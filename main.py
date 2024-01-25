import cv2
import face_recognition
import numpy as np
import interface

cap = cv2.VideoCapture(0)

FLAG_ENTRY_OR_AUTHENTICATE = interface.thumbnail()
FLAG_ENTRY_NUMBER = 0

# 登録用
if FLAG_ENTRY_OR_AUTHENTICATE == 1:
    counter = 0
    images = []
    ids = []
    trainerPath = 'trainer/trainer.yml'
    
    face_angle_checker = face_recognition.FaceAngleChecker()

    while True:

        ret, img = cap.read()
        if ret :
            cv2.imshow('Entry', img)
            auth = face_recognition.entry(img)
            detected = auth.detect()
                        
            if detected is not None and len(detected) > 0:
                angles = face_angle_checker.check_degree(detected)
                if angles is not None:
                    # print("Pitch: {:.2f}, Yaw: {:.2f}, Roll: {:.2f}".format(*angles))
                    if FLAG_ENTRY_NUMBER == 0:
                        if angles[0] > 10.5 and angles[0] < 11.5 and angles[2] > 160 and angles[2] < 180:
                            # images.append(detected)
                            # ids.append(0)
                            FLAG_ENTRY_NUMBER += 1
                            print('正面OK')
                            detectedHSV = cv2.cvtColor(detected, cv2.COLOR_BGR2HSV)
                            h, s, v = cv2.split(detectedHSV)
                            vChanged = np.zeros(int(v.size))
                            for i in range(1, 10):
                                vChanged = v / i
                                vChanged = np.clip(vChanged, 0, 255).astype(np.uint8)
                                mergedImage = cv2.cvtColor(cv2.merge((h, s, vChanged)), cv2.COLOR_HSV2BGR)
                                cv2.imshow("Changed" + str(i), mergedImage)
                                while(1):
                                    key = cv2.waitKey(1)
                                    if key==ord('q'):
                                        break
                                images.append(mergedImage)
                                ids.append(i)
                            auth.register(trainerPath, images, ids)
                            break
                
        key = cv2.waitKey(1)
        if key==ord('q'):
            break

# 認証用
elif FLAG_ENTRY_OR_AUTHENTICATE == 2:
    counter = 0
    images = []
    ids = []
    trainerPath = 'trainer/trainer.yml'

    while True:

        ret, img = cap.read()

        if ret:
            recognized = face_recognition.authentication(trainerPath).recognize(img)
            cv2.imshow('recognized', recognized)
                
        key = cv2.waitKey(1)
        if key==ord('q'):
            break


cap.release()
cv2.destroyAllWindows()
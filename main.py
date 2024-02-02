import cv2
import face_recognition
import numpy as np
import interface
import tkinter as tk
from tkinter import messagebox as msgbox

cap = cv2.VideoCapture(0)

FLAG_ENTRY_OR_AUTHENTICATE = interface.thumbnail()
FLAG_ENTRY_NUMBER = 0

# print(FLAG_ENTRY_OR_AUTHENTICATE)

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
                if angles is not None :
                    # print("Yaw: {:.2f}, Pitch: {:.2f}, Roll: {:.2f}".format(*angles))
                    pitch = angles[1]
                    yaw = angles[0]
                    roll = angles[2]
                    # Pitch: 顔の上下
                    # Yaw: 顔の左右
                    # Roll: 顔の傾斜
                    if FLAG_ENTRY_NUMBER == 0:
                        if pitch > -5 and pitch < 5 and yaw > -5 and yaw < 5:
                            detectedHSV = cv2.cvtColor(detected, cv2.COLOR_BGR2HSV)
                            h, s, v = cv2.split(detectedHSV)
                            v_mean = v.mean()
                            if v_mean > 100:
                                vChanged = np.zeros(int(v.size))
                                for i in range(1, 10):
                                    vChanged = v / i
                                    vChanged = np.clip(vChanged, 0, 255).astype(np.uint8)
                                    mergedImage = cv2.cvtColor(cv2.merge((h, s, vChanged)), cv2.COLOR_HSV2BGR)
                                    # cv2.imshow("Changed" + str(i), mergedImage)
                                    images.append(mergedImage)
                                    ids.append(i)
                                FLAG_ENTRY_NUMBER += 1
                                # interface.caution(640, 320, '正面の画像を取得しました', 40,
                                #                    '次は「右」を向いてください.', 100)
                                msgbox.showinfo('画像取得完了(正面)', '正面の画像を取得しました. 次は「右」を向いてください.')
                            else:
                                print("Caution!")
                    elif FLAG_ENTRY_NUMBER == 1:
                        if pitch > -10 and pitch < 10 and yaw > -90 and yaw < -20:
                            detectedHSV = cv2.cvtColor(detected, cv2.COLOR_BGR2HSV)
                            h, s, v = cv2.split(detectedHSV)
                            v_mean = v.mean()
                            if v_mean > 100:
                                vChanged = np.zeros(int(v.size))
                                for i in range(1, 10):
                                    vChanged = v / i
                                    vChanged = np.clip(vChanged, 0, 255).astype(np.uint8)
                                    mergedImage = cv2.cvtColor(cv2.merge((h, s, vChanged)), cv2.COLOR_HSV2BGR)
                                    # cv2.imshow("Changed" + str(i), mergedImage)
                                    images.append(mergedImage)
                                    ids.append(i)
                                FLAG_ENTRY_NUMBER += 1
                                # interface.caution(640, 320, '右向きの画像を取得しました', 40,
                                #                    '次は「左」を向いてください.', 100)
                                msgbox.showinfo('画像取得完了(右)', '右向きの画像を取得しました. 次は「左」を向いてください.')

                    elif FLAG_ENTRY_NUMBER == 2:
                        if pitch > -10 and pitch < 10 and yaw > 20 and yaw < 90:
                            detectedHSV = cv2.cvtColor(detected, cv2.COLOR_BGR2HSV)
                            h, s, v = cv2.split(detectedHSV)
                            v_mean = v.mean()
                            if v_mean > 100:
                                vChanged = np.zeros(int(v.size))
                                for i in range(1, 10):
                                    vChanged = v / i
                                    vChanged = np.clip(vChanged, 0, 255).astype(np.uint8)
                                    mergedImage = cv2.cvtColor(cv2.merge((h, s, vChanged)), cv2.COLOR_HSV2BGR)
                                    # cv2.imshow("Changed" + str(i), mergedImage)
                                    images.append(mergedImage)
                                    ids.append(i)
                                FLAG_ENTRY_NUMBER += 1
                                auth.register(trainerPath, images, ids)
                                # interface.caution(640, 320, '左向きの画像を取得しました', 40,
                                #                    '顔画像登録が完了しました. 再起動してください. ', 100)
                                msgbox.showinfo('画像取得完了(左)', '左の画像を取得しました. 顔画像登録が完了しました. 再起動してください. ')
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
        cv2.imshow('Authenticating...', img)

        if ret:
            recognized, confidence = face_recognition.authentication(trainerPath).recognize(img)
            if confidence is not None:
                if confidence > 60:
                    interface.authenticated()
                    break
                
        key = cv2.waitKey(1)
        if key==ord('q'):
            break


cap.release()
cv2.destroyAllWindows()
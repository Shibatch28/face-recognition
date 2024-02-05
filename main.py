import cv2
import face_recognition
import numpy as np
import interface
import tkinter as tk
from tkinter import messagebox as msgbox

cap = cv2.VideoCapture(2)

FLAG_ENTRY_OR_AUTHENTICATE = interface.thumbnail()
FLAG_ENTRY_NUMBER = 0

# print(FLAG_ENTRY_OR_AUTHENTICATE)
face_angle_checker = face_recognition.FaceAngleChecker()

# 登録用
if FLAG_ENTRY_OR_AUTHENTICATE == 1:
    counter = 0
    images = []
    ids = []
    trainerPath = 'trainer/trainer.yml'
    

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

    FLAG_AUTHENTICATE_NUMBER = 0
    center_yaw = 0
    center_pitch = 0
    min_yaw = 0
    max_yaw = 0
    min_pitch = 0
    min_pitch = 0

    while True:

        ret, img = cap.read()
        cv2.imshow('Authenticating...', img)

        
        if ret:
            recognized, confidence = face_recognition.authentication(trainerPath).recognize(img)
            auth = face_recognition.entry(img)
            detected = auth.detect()
            if detected is not None and len(detected) > 0:
                angles = face_angle_checker.check_degree(detected)
                if angles is not None :
                    print("Yaw: {:.2f}, Pitch: {:.2f}, Roll: {:.2f}".format(*angles))
                    pitch = angles[1]
                    yaw = angles[0]
                    roll = angles[2]
                    # Pitch: 顔の上下
                    # Yaw: 顔の左右
                    # Roll: 顔の傾斜
                    if FLAG_AUTHENTICATE_NUMBER == 0:
                        if confidence is not None:
                            print(confidence)
                            if confidence > 60:
                                # interface.authenticated()
                                msgbox.showinfo('第一次認証完了', '第一次認証が完了しました．顔を左右上下に動かしてください．')
                                center_yaw = yaw
                                center_pitch = pitch
                                min_yaw = yaw
                                min_pitch = pitch
                                max_yaw = yaw
                                max_pitch = pitch
                                FLAG_AUTHENTICATE_NUMBER = 1
                    elif FLAG_AUTHENTICATE_NUMBER == 1:
                        if yaw < min_yaw:
                            min_yaw = yaw
                        if yaw > max_yaw:
                            max_yaw = yaw
                        if pitch < min_pitch:
                            min_pitch = pitch
                        if pitch > max_pitch:
                            max_pitch = pitch
                        if max_yaw - min_yaw >= 30 and max_pitch - min_pitch >=5:
                            msgbox.showinfo('第二次認証完了', '第二次認証が完了しました．アプリケーションを終了します．')
                            break
                        
                    
                
        key = cv2.waitKey(1)
        if key==ord('q'):
            break


cap.release()
cv2.destroyAllWindows()
import cv2
import numpy as np
from PIL import Image
import os

class entry:
    def __init__(self, frame):
        self.frame = frame  # カメラから取得した画像
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def register(self):
        # グレースケール化
        gray = cv2.cvtColor(self.frame. cv2.COLOR_BGR2GRAY)
        # 顔検出
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)

        # 画像面積が一番大きいものを抜き出す
        size = []
        for (w, h) in faces:
            size.append(w * h)
        
        # 最大値を探す
        maxSize = size.max()
        maxIndex = size.index(maxSize)
        
        returnFace = faces[maxIndex]

        cv2.rectangle(self.frame (returnFace.x, returnFace.y), (returnFace.x + returnFace.w, returnFace.y + returnFace.h), (255, 0, 0), 2)

        # # 検出された顔に矩形を描画
        # for (x, y, w, h) in faces:
        #     cv2.rectangle(self.frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        




class authentication:
    def __init__(self):
        pass

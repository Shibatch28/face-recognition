import cv2
import copy
import numpy as np

'''

画像登録用のクラス: entry

'''
class entry(object):
    def __init__(self, frame):
        self.frame = frame  # カメラから取得した画像
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def detect(self):
        # グレースケール化
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        # 顔検出
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)

        # 画像面積が一番大きいものを抜き出す
        size = []
        for (x, y, w, h) in faces:
            size.append(w * h)
        
        # 最大値を探す
        if len(size) > 0:
            maxSize = max(size)
            maxIndex = size.index(maxSize)
            
            recognizedFace = faces[maxIndex]
            returnFace = self.frame[recognizedFace[1]:recognizedFace[1] + recognizedFace[3] - 1, 
                                    recognizedFace[0]:recognizedFace[0] + recognizedFace[2] - 1]

            return returnFace
        else:
            return None

    def register(self, path, images, ids):
        # LBPHFaceRecognizerのインスタンスを作成
        images = [cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) for img in images]
        ids = np.array(ids)
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        for i in range(len(images)):
            images[i] = cv2.cvtColor(images[i], cv2.COLOR_BGR2GRAY)
        recognizer.train(images, ids)
        recognizer.write(path)

'''

画像取得用のクラス authentication

'''

class authentication(object):
    def __init__(self, path):
        self.path = path
    
    def recognize(self, frame):
        # トレーニング済みのモデルをロード
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        font = cv2.FONT_HERSHEY_SIMPLEX

        recognizer.read(self.path)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (30, 30),
        )

        result = copy.deepcopy(frame)

        for(x,y,w,h) in faces:
            # cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

            # 確信度が低い場合はラベルとしてUnknownを表示
            if (confidence < 100):
                id = f"ID: {id}"
                confidence = f"  {round(100 - confidence)}%"
            else:
                id = "Unknown"
                confidence = f"  {round(100 - confidence)}%"
            
            cv2.putText(result, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
            cv2.putText(result, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1) 
        
        return result
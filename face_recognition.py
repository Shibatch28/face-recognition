import cv2
import copy
import numpy as np
import dlib
from imutils import face_utils

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
        
    def checkDegree(self, frame):
        detector = dlib.get_frontal_face_detector()
        face_rects = detector(frame, 0)
        face_landmark_path = './shape_predictor_68_face_landmarks.dat'
        predictor = dlib.shape_predictor(face_landmark_path)


    def register(self, path, images, ids):
        # LBPHFaceRecognizerのインスタンスを作成
        images = [cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) for img in images]
        ids = np.array(ids)
        recognizer = cv2.face.LBPHFaceRecognizer_create()
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
        return_confidence = None

        for(x,y,w,h) in faces:
            # cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            return_confidence = round(100 - confidence)

            # 確信度が低い場合はラベルとしてUnknownを表示
            if (confidence < 100):
                id = f"ID: {id}"
                confidence = f"  {round(100 - confidence)}%"
            else:
                id = "Unknown"
                confidence = f"  {round(100 - confidence)}%"
            
            cv2.putText(result, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
            cv2.putText(result, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1) 
        
        return result, return_confidence


class FaceAngleChecker:
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor('./shape_predictor_68_face_landmarks.dat')

    def get_landmarks(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray)
        if len(faces) == 0:
            return None
        return self.predictor(gray, faces[0])

    def calculate_angle(self, landmarks):
        # 目の中心点
        left_eye_center = np.array([landmarks.part(36).x, landmarks.part(36).y])
        right_eye_center = np.array([landmarks.part(45).x, landmarks.part(45).y])
        mid_eye_point = (left_eye_center + right_eye_center) / 2

        # 鼻先の点
        nose_point = np.array([landmarks.part(30).x, landmarks.part(30).y])

        # 耳の近くの点（ヨー角計算用）
        left_side_point = np.array([landmarks.part(0).x, landmarks.part(0).y])
        right_side_point = np.array([landmarks.part(16).x, landmarks.part(16).y])

        # ロール角（顔の傾斜）を計算
        roll = np.arctan2(right_eye_center[1] - left_eye_center[1], right_eye_center[0] - left_eye_center[0])

        # ピッチ角（顔の上下の向き）を計算
        pitch = np.arctan2(mid_eye_point[1] - nose_point[1], nose_point[0] - mid_eye_point[0])

        # ヨー角（顔の左右の向き）を計算
        yaw = np.arctan2(right_side_point[0] - left_side_point[0], right_side_point[1] - left_side_point[1])

        return np.degrees(pitch) + 90, np.degrees(yaw) - 90, np.degrees(roll)

    def check_degree(self, frame):
        landmarks = self.get_landmarks(frame)
        if landmarks is None:
            return None
        return self.calculate_angle(landmarks)

# 使用例
# face_angle_checker = FaceAngleChecker()
# frame = cv2.imread('path_to_image.jpg')  # 画像を読み込む
# angles = face_angle_checker.check_degree(frame)
# if angles is not None:
#     print("Pitch: {:.2f}, Yaw: {:.2f}, Roll: {:.2f}".format(*angles))

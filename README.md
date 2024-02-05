# Face Recognizer ver 1.0

## 前提
このアプリケーションはdlib, numpy, OpenCV, Tkinterを使用します. 
また, 学習済みデータとしてshape_predictor_68_face_landmarks.datを使用しますので, DLしておいてください. 

```
pip install dlib
pip install numpy
pip install opencv-contrib-python
pip install tkinter
```

学習済みデータ: [dlib.net](http://dlib.net/files/)

## 使用方法
* main.pyを実行します. ウィンドウ起動ののち, Entryを押せば画像登録開始となります.
* 画像取得は「正面」「右」「左」の順番となります. 
* 全ての画像を取得したら一度アプリケーションが閉じますので, 再起動してください. 
* 再起動した後, Authenticateを押せば認証開始となります. 
* 正面を向いた後, 顔を動かすことで認証できます. 

## 余談
そのうちJavaで書き直そうと思っています. 

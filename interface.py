import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()

FLAG_ENTRY_OR_AUTHENTICATE = 0

WINDOW_FONT = 'FOT-UD角ゴ_ラージ Pr6N'
# WINDOW_FONT = 'MS P Gothic'

def center(window, button, y):
    window.update()  # ウィンドウを更新して描画を完了させる
    window.update_idletasks()  # ウィンドウの現在のサイズを取得するために必要
    width = window.winfo_width()
    button_width = button.winfo_width()
    print(button_width)
    x = (width - button_width) // 2
    button.place(x=x, y=y)

def entrySet():
    global FLAG_ENTRY_OR_AUTHENTICATE
    FLAG_ENTRY_OR_AUTHENTICATE = 1
    root.destroy()

def authenticateSet():
    global FLAG_ENTRY_OR_AUTHENTICATE
    FLAG_ENTRY_OR_AUTHENTICATE = 2
    root.destroy()

def thumbnail():
    global root
    root.title(u"Face Authenticator")
    root.geometry("640x480")

    # 画像の読み込みと背景に設定
    background_image = Image.open("src/thumbnail.png")  # 画像パスを指定
    background_photo = ImageTk.PhotoImage(background_image)

    background_label = tk.Label(root, image=background_photo)
    background_label.place(relwidth=1, relheight=1)

    entryButton = tk.Button(root, text="Entry", font=(WINDOW_FONT, '20'), command=entrySet)
    entryButton.pack()
    center(root, entryButton, 320)

    authenticateButton = tk.Button(root, text="Authenticate", font=(WINDOW_FONT, '20'), command=authenticateSet)
    authenticateButton.pack()
    center(root, authenticateButton, 380)

    root.mainloop()

    return FLAG_ENTRY_OR_AUTHENTICATE

def authenticated():
    pass
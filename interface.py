import tkinter as tk
import winsound
from PIL import Image, ImageTk

FAVICON_FILE = 'src/favicon.ico'
FLAG_ENTRY_OR_AUTHENTICATE = 0
WINDOW_FONT = 'FOT-UD角ゴ_ラージ Pr6N'
# WINDOW_FONT = 'MS P Gothic'

def center(window, button, y):
    window.update()  # ウィンドウを更新して描画を完了させる
    window.update_idletasks()  # ウィンドウの現在のサイズを取得するために必要
    width = window.winfo_width()
    button_width = button.winfo_width()
    x = (width - button_width) // 2
    button.place(x=x, y=y)

def entrySet(root):
    global FLAG_ENTRY_OR_AUTHENTICATE
    FLAG_ENTRY_OR_AUTHENTICATE = 1
    root.destroy()

def authenticateSet(root):
    global FLAG_ENTRY_OR_AUTHENTICATE
    FLAG_ENTRY_OR_AUTHENTICATE = 2
    root.destroy()

def IsOk(root):
    root.destroy()

def thumbnail():
    root = tk.Tk()
    root.iconbitmap(default=FAVICON_FILE)
    root.title(u"Face Recognizer")
    root.geometry("640x480")

    # 画像の読み込みと背景に設定
    background_image = Image.open("src/thumbnail.png")  # 画像パスを指定
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = tk.Label(root, image=background_photo)
    background_label.place(relwidth=1, relheight=1)

    entryButton = tk.Button(root, text="Entry", font=(WINDOW_FONT, '20'), command=lambda:entrySet(root))
    entryButton.pack()
    center(root, entryButton, 320)
    
    authenticateButton = tk.Button(root, text="Authenticate", font=(WINDOW_FONT, '20'), command=lambda:authenticateSet(root))
    authenticateButton.pack()
    center(root, authenticateButton, 380)

    root.mainloop()

    return FLAG_ENTRY_OR_AUTHENTICATE

def caution(width, height, head, head_y, message, message_y):
    # winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
    # root = tk.Tk()
    # root.iconbitmap(default=FAVICON_FILE)
    # root.title(u"Face Recognizer")
    # root.geometry(str(width)+'x'+str(height))
    # hd = tk.Label(root, text=head, font=(WINDOW_FONT, '32'))
    # hd.pack()
    # center(root, hd, head_y)
    # msg = tk.Label(root, text=message, font=(WINDOW_FONT, '16'))
    # msg.pack()
    # center(root, msg, message_y)
    # OKbutton = tk.Button(root, text="OK", font=(WINDOW_FONT, '16'), command=lambda:IsOk(root))
    # OKbutton.pack()
    # center(root, OKbutton, height - 100)

    # root.mainloop()

    # return 0
    pass


    

def authenticated():
    winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
    root = tk.Tk()
    root.iconbitmap(default=FAVICON_FILE)
    root.title(u"Face Recognizer")
    root.geometry("400x200")
    hd = tk.Label(root, text=u"認証完了", font=(WINDOW_FONT, '32'))
    hd.pack()
    center(root, hd, 40)
    root.mainloop()
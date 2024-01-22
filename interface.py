import tkinter as tk

def thumbnail():
    root = tk.Tk()
    root.title(u"Face Authenticator")
    root.geometry("640x480")

    # ファイルを参照
    background = tk.PhotoImage(file="src/thumbnail.png")

    bg = tk.Label(root, image=background)
    bg.pack(fill="x")

    root.mainloop()

def authenticated():
    pass
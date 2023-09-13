import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
root.title('oxxo.studio')
root.geometry('200x200')

img = Image.open('shake-hands.png')        # 開啟圖片
tk_img = ImageTk.PhotoImage(img)    # 轉換為 tk 圖片物件

label = tk.Label(root, image=tk_img, width=200, height=200)  # 在 Lable 中放入圖片
label.pack()

root.mainloop()
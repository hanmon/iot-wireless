import tkinter as tk

root = tk.Tk()
root.title('oxxo.studio')
root.geometry('200x200')

a = tk.StringVar()   # 建立文字變數
a.set('')            # 一開始設定沒有內容

tk.Label(root, textvariable=a).pack()  # 放入 Label
tk.Entry(root, textvariable=a).pack()  # 放入 Entry

root.mainloop()
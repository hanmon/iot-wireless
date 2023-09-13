import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title('oxxo.studio')
root.geometry('200x200')

bar = ttk.Progressbar(root, mode='determinate')
bar.pack(pady=10)

a = 0                       # 設定 a 從 0 開始
def show():
    global a                # 設定 a 是全域變數
    if a< bar['maximum']:
        a = a + 10          # 如果 a 小於進度條的最大值
        bar['value'] = a    # 設定進度條 value 為 a
        val.set(f'{a}%')    # Lable 變數設為 a

val = tk.StringVar()
val.set('0%')

label = tk.Label(root, textvariable=val)
label.pack()

button = tk.Button(root, text='增加進度', command=show)
button.pack()

root.mainloop()
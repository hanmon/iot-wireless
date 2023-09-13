import os
os.chdir('/')       # 移動路徑到根目錄

import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.title('oxxo.studio')
root.geometry('200x200')

text = tk.StringVar()   # 設定 text 為文字變數
text.set('')            # 設定 text 的內容

def show():
    file_path = filedialog.askopenfilename()
    f = open(file_path,'r')      # 根據檔案路徑開啟檔案
    a = f.read()                 # 讀取檔案內容
    text.set(a)                  # 設定變數為檔案內容
    f.close()                    # 關閉檔案

# Button 設定 command 參數
btn = tk.Button(root,
                text='我是按鈕',
                font=('Arial',20,'bold'),
                command=show
              )
btn.pack()

mylabel = tk.Label(root, textvariable=text, font=('Arial',20))  # 放入標籤，使用 textvariable=text
mylabel.pack()

root.mainloop()
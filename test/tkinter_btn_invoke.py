import tkinter as tk

root = tk.Tk()
root.title('oxxo.studio')
root.geometry('200x200')

n = 0               # n 等於 0
a = tk.StringVar()  # 設定 a 為文字變數
a.set(n)            # 設定 a 的內容

def add():
    global n        # n 是全域變數
    n = n + 1       # 每次執行 add 時將 n 增加 1
    a.set(n)        # 設定 a 的內容

mylabel = tk.Label(root, textvariable=a, font=('Arial',20))  # 放入標籤
mylabel.pack()

# Button 設定 command 參數
btn = tk.Button(root,
                text='我是按鈕',
                font=('Arial',30,'bold'),
                command=add
              )
btn.pack()

for i in range(4):
    btn.invoke()

root.mainloop()
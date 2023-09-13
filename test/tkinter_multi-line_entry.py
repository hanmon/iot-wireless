import tkinter as tk

root = tk.Tk()
root.title('oxxo.studio')
root.geometry('200x200')

a = tk.StringVar()   # 建立文字變數
a.set('')            # 一開始設定沒有內容

label = tk.Label(root, textvariable=a)  # 放入 Label
label.pack()

text = tk.Text(root, height=8)  # 放入多行輸入框
text.pack()

def show():
    a.set(text.get(1.0, 'end-1c'))
    # 執行 show 函式時，將 a 變數內容改變
    # 使用 end-1c 表示取得倒數第二個字元 ( 因為最後一個字元是換行符 )

def clear():
    a.set('')
    text.delete(1.0,'end')
    # 執行 clear 函式時，清空內容

btn1 = tk.Button(root,text='show', command=show)    # 放入顯示按鈕
btn1.pack()

btn2 = tk.Button(root,text='clear', command=clear)  # 放入清空按鈕
btn2.pack()

root.mainloop()
import tkinter as tk
import datetime

# 定義產生不同時區時間的函式
def timezone(h):
    GMT = datetime.timezone(datetime.timedelta(hours=h))      # 取得時區
    now = datetime.datetime.now(tz=GMT).strftime('%H:%M:%S')  # 取得該時區的時間
    return now

root = tk.Tk()
root.title('oxxo.studio')
root.geometry('200x300')

name = ['倫敦','台灣','日本','紐約']          # 四個時區的名稱串列
loc_time = [1,8,9,-4]                      # 四個時區的 GMT 數字
arr = [tk.StringVar() for i in range(4)]   # 使用串列生成式，產生一個內容包含四個 tk 文字變數的串列

# 定義顯示時間的函式
def showTime():
    # 因為有四個時區，使用 for 迴圈執行四次
    for i in range(4):
        arr[i].set(timezone(loc_time[i]))  # 設定文字變數
    root.after(1000, showTime)             # 視窗每隔 1000 毫秒再次執行一次 showTime()

# 因為有四個時區，使用 for 迴圈執行四次
for i in range(4):
    # 依序加入不同時區的名稱與時間
    tk.Label(root, text=name[i], font=('Arial',20)).pack()
    tk.Label(root, textvariable=arr[i], font=('Arial',20)).pack()

showTime()

root.mainloop()
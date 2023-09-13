import tkinter as tk
import datetime

GMT = datetime.timezone(datetime.timedelta(hours=8))    # 設定所在時區 ( 台灣是 GMT+8 )

root = tk.Tk()                # 建立視窗物件
root.title('oxxo.studio')     # 設定視窗標題
root.geometry('200x200')      # 設定視窗大小

a = tk.StringVar()            # 建立文字變數

# 建立不斷改變文字變數的函式
def showTime():
    now = datetime.datetime.now(tz=GMT).strftime('%H:%M:%S')   # 取得目前的時間，格式使用 H:M:S
    a.set(now)                    # 設定變數內容
    root.after(1000, showTime)    # 視窗每隔 1000 毫秒再次執行一次 showTime()

tk.Label(root, text='目前時間', font=('Arial',20)).pack()   # 放入第一個 Label 標籤
tk.Label(root, textvariable=a, font=('Arial',20)).pack()   # 放入第二個 Label 標籤，內容是 a 變數

showTime()   # 執行函式

root.mainloop()
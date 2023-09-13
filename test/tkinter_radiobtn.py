import tkinter as tk

root = tk.Tk()
root.title('oxxo.studio')
root.geometry('200x200')

radio_btn1 = tk.Radiobutton(root, text='Apple')    # 放入第一個單選按鈕
radio_btn1.pack()

radio_btn2 = tk.Radiobutton(root, text='Banana')   # 放入第二個單選按鈕
radio_btn2.pack()

root.mainloop()
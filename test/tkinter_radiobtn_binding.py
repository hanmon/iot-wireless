import tkinter as tk

root = tk.Tk()
root.title('oxxo.studio')
root.geometry('200x200')

val = tk.StringVar()

radio_btn1 = tk.Radiobutton(root, text='Apple',variable=val, value='Apple')
radio_btn1.pack()
radio_btn1.select()  # 搭配 select() 方法選取 radio_btn1

radio_btn2 = tk.Radiobutton(root, text='Banana',variable=val, value='Banana')
radio_btn2.pack()

mylabel = tk.Label(root, textvariable=val, font=('Arial',20))  # 放入標籤
mylabel.pack()

root.mainloop()
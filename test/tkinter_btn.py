import tkinter as tk

root = tk.Tk()
root.title('oxxo.studio')
root.geometry('200x200')

btn = tk.Button(root,
                text='我是按鈕',
                font=('Arial',30,'bold'),
                padx=10,
                pady=10,
                activeforeground='#f00'
              )
btn.pack()

root.mainloop()
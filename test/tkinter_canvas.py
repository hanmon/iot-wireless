import tkinter as tk

root = tk.Tk()
root.title('oxxo.studio')
root.geometry('300x300')

canvas = tk.Canvas(root, width=300, height=300)
canvas.create_text(10, 0, text='hello', anchor='nw')
canvas.create_text(20, 20, text='world', anchor='nw', font=('Arial', 20))
canvas.create_text(30, 40, text='I am\nOXXO', anchor='nw', fill='#f00', font=('Arial', 30, 'bold'))
canvas.create_text(40, 110, text='中文測試', anchor='nw', fill='#0a0', font=('Arial', 30, 'bold','italic','underline'))
canvas.pack()

root.mainloop()
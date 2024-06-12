from tkinter import *

def open_data_window():
    data_window = Toplevel()
    toplevel_width = 300
    toplevel_height = 300
    data_window.geometry(f"{toplevel_width}x{toplevel_height}")
    data_window.resizable( width=False ,height=False )

    # Создание текста
    label = Label(data_window, text="Enter cosmic bodie parametrs")
    label.pack()
    
    label_type = Label(data_window, text="type :")
    label_type.place(x=20,y=20)
    
    label_type = Label(data_window, text="type :")
    label_type.place(x=20,y=20)
    

    # Создание поля для ввода
    entry = Entry(data_window)
    entry.pack()

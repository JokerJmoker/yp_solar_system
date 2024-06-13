from tkinter import *
from solar_main import *
from solar_objects import *
from solar_input import *
from solar_vis import *
from solar_model import *
import os


# Путь к файлу в корневой папке проекта
file_path = os.path.join(os.getcwd(), 'cosmic_bodies.txt')


def save_data_to_file():
    type_value = entry_type.get()
    radius_value = entry_radius.get()
    color_value = entry_color.get()
    x_value = entry_x.get()
    y_value = entry_y.get()
    V_tg_value = entry_V_tg.get()
    ID_value = entry_ID.get()
    
    data_line = f"{type_value} {radius_value} {color_value} {x_value} {y_value} {V_tg_value} {ID_value}\n"

    with open(file_path, 'a') as file:
        file.write(data_line)


def show_uploaded_cosmic_bodies():
    pass
#FIXME здесь надо добавить метод (по аналогии с open_file_dialog() , только не с полным набором используемых функций) по отрисовке объектов на холсте space


def open_data_window():
    global entry_type, entry_radius, entry_color, entry_x , entry_y, entry_V_tg, entry_ID
    
    data_window = Toplevel()
    toplevel_width = 300
    toplevel_height = 400
    data_window.geometry(f"{toplevel_width}x{toplevel_height}+200+500")
    data_window.resizable(width=False, height=False)

    label_text = Label(data_window, text="Enter cosmic body's parameters:")
    label_text.pack(side=TOP)

    label_star = Label(data_window, text="Star: type r color x y ID_ST ")
    label_star.place(x =10, y = 275)
    
    label_star = Label(data_window, text="Planet: type r color x y ID_ROT ID_ST ")
    label_star.place(x =10, y = 300)

    label_star = Label(data_window, text="Satelite: type r color x y ID_ROTx ID_STx2 ")
    label_star.place(x =10, y = 325)


    label_type = Label(data_window, text="Type:")
    label_type.place(x=10, y=40)
    entry_type = Entry(data_window)
    entry_type.place(x=100, y=40)

    label_radius = Label(data_window, text="Radius:")
    label_radius.place(x=10, y=70)
    entry_radius = Entry(data_window)
    entry_radius.place(x=100, y=70)

    label_color = Label(data_window, text="Color:")
    label_color.place(x=10, y=100)
    entry_color = Entry(data_window)
    entry_color.place(x=100, y=100)

    label_x = Label(data_window, text="x:")
    label_x.place(x=10, y=130)
    entry_x = Entry(data_window)
    entry_x.place(x=100, y=130)

    label_y = Label(data_window, text="y:")
    label_y.place(x=10, y=160)
    entry_y = Entry(data_window)
    entry_y.place(x=100, y=160)

    label_V_tg = Label(data_window, text="V_tg:")
    label_V_tg.place(x=10, y=190)
    entry_V_tg = Entry(data_window)
    entry_V_tg.place(x=100, y=190)

    label_ID_for_rotating = Label(data_window, text="ID_ROT:")
    label_ID_for_rotating.place(x=10, y=220)
    entry_ID_for_rotating = Entry(data_window)
    entry_ID_for_rotating.place(x=100, y=220)

    label_ID_for_static = Label(data_window, text="ID_ST:")
    label_ID_for_static.place(x=10, y=250)
    entry_ID_for_static = Entry(data_window)
    entry_ID_for_static.place(x=100, y=250)

    upload_button = Button(data_window, text="Upload", command=save_data_to_file)
    upload_button.place(x=50, y=355)

    show_button = Button(data_window, text="Show", command=show_uploaded_cosmic_bodies)
    show_button.place(x=200, y=355)


if __name__ == "__main__":
    print("This module is not for direct call!")

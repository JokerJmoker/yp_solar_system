from tkinter import *
import os

# Глобальные переменные для полей ввода
entry_type = None
entry_radius = None
entry_color = None
entry_x = None
entry_y = None
entry_V_tg = None
entry_ID = None

# Путь к файлу в корневой папке проекта
file_path = os.path.join(os.getcwd(), 'cosmic_bodies.txt')

def save_data_to_file():
    global entry_type, entry_radius, entry_color, entry_x, entry_y, entry_V_tg, entry_ID

    # Получить данные из глобальных переменных полей ввода
    type_value = entry_type.get()
    radius_value = entry_radius.get()
    color_value = entry_color.get()
    x_value = entry_x.get()
    y_value = entry_y.get()
    V_tg_value = entry_V_tg.get()
    ID_value = entry_ID.get()

    # Формирование строки для записи в файл
    data_line = f"{type_value} {radius_value} {color_value} {x_value} {y_value} {V_tg_value} {ID_value}\n"

    # Записать данные в файл
    with open(file_path, 'a') as file:
        file.write(data_line)

def open_data_window():
    global entry_type, entry_radius, entry_color, entry_x, entry_y, entry_V_tg , entry_ID

    data_window = Toplevel()
    toplevel_width = 300
    toplevel_height = 300
    data_window.geometry(f"{toplevel_width}x{toplevel_height}")
    data_window.resizable(width=False, height=False)

    # Создание текста и размещение его в окне
    label_text = Label(data_window, text="Enter cosmic bodie's paramets:")
    label_text.pack(side=TOP)

    # Создание меток и полей ввода
    label_type = Label(data_window, text="type:")
    label_type.place(x=20, y=40)
    entry_type = Entry(data_window)
    entry_type.place(x=100, y=40)

    label_radius = Label(data_window, text="R:")
    label_radius.place(x=20, y=70)
    entry_radius = Entry(data_window)
    entry_radius.place(x=100, y=70)

    label_color = Label(data_window, text="color:")
    label_color.place(x=20, y=100)
    entry_color = Entry(data_window)
    entry_color.place(x=100, y=100)

    label_x = Label(data_window, text="x:")
    label_x.place(x=20, y=130)
    entry_x = Entry(data_window)
    entry_x.place(x=100, y=130)

    label_y = Label(data_window, text="y:")
    label_y.place(x=20, y=160)
    entry_y = Entry(data_window)
    entry_y.place(x=100, y=160)

    label_V_tg = Label(data_window, text="V_tg:")
    label_V_tg.place(x=20, y=190)
    entry_V_tg = Entry(data_window)
    entry_V_tg.place(x=100, y=190)

    label_ID = Label(data_window, text="ID:")
    label_ID.place(x=20, y=220)
    entry_ID = Entry(data_window)
    entry_ID.place(x=100, y=220)

    # Кнопка для сохранения данных в файл
    save_button = Button(data_window, text="Save", command=save_data_to_file)
    save_button.pack(side=BOTTOM)

if __name__ == "__main__":
    print("This module is not for direct call!")
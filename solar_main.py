# coding: utf-8
# license: GPLv3

import tkinter
from tkinter import *
from tkinter.filedialog import *
from solar_vis import *
from solar_model import *
from solar_input import *
from data_window import *
from solar_objects import OrbitManager

perform_execution = False
"""Флаг цикличности выполнения расчёта"""

physical_time = 0
"""Физическое время от начала расчёта.
Тип: float"""

displayed_time = None
"""Отображаемое на экране время.
Тип: переменная tkinter"""

time_step = None
"""Шаг по времени при моделировании.
Тип: float"""

space_objects = []
"""Список космических объектов."""

show_orbits = False
"""Флаг для переключения состояний орбит(show/hide)"""

orbit_manager = None
"""Создание экземпляра класса OrbitManager для обработки используемых методов """


def toggle_orbits():
    global show_orbits

    if orbits_button['text'] == "Show orbits":
        orbits_button['text'] = "Hide orbits"
        show_orbits = True
        orbit_manager.update_orbit_images(space_objects)
    else:
        orbits_button['text'] = "Show orbits"
        show_orbits = False
        orbit_manager.clear_orbit_images()

#FIXME "1" настроить правильную обработку нажатия кнопки мыши и передачи кординат крусора в модуль data_window в качестве значений enter_x и enter_y
"""        
def handle_right_click(event):
        mouse_x = event.x
        mouse_y = event.y
        update_entry_values(mouse_x, mouse_y)

          
def update_entry_values(x, y):
    entry_x.set(x)
    entry_y.set(y)
"""

def execution():
    """Функция исполнения -- выполняется циклически, вызывая обработку всех небесных тел,
    а также обновляя их положение на экране.
    Цикличность выполнения зависит от значения глобальной переменной perform_execution.
    При perform_execution == True функция запрашивает вызов самой себя по таймеру через от 1 мс до 100 мс.
    """
    global physical_time
    global displayed_time
    recalculate_space_objects_positions(space_objects, time_step.get())

    for body in space_objects:
        update_object_position(space, body) 
        
        if show_orbits: # остлеживает флаг , относящийся к отображению орбит
            orbit_manager.update_orbit_images(space_objects)
        
    physical_time += time_step.get()
    displayed_time.set("%.1f" % physical_time + " seconds gone")

    if perform_execution:
        space.after(101 - int(time_speed.get()), execution)


def start_execution():
    """Обработчик события нажатия на кнопку Start.
    Запускает циклическое исполнение функции execution.
    """
    global perform_execution
    perform_execution = True
    start_button['text'] = "Pause"
    start_button['command'] = stop_execution

    execution()
    print('Started execution...')


def stop_execution():
    """Обработчик события нажатия на кнопку Start.
    Останавливает циклическое исполнение функции execution.
    """
    global perform_execution
    perform_execution = False
    start_button['text'] = "Start"
    start_button['command'] = start_execution
    print('Paused execution.')


def open_file_dialog():
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    global space_objects
    global perform_execution
    perform_execution = False
    for obj in space_objects:
        space.delete(obj.image)  # удаление старых изображений планет
    in_filename = askopenfilename(filetypes=(("Text file", ".txt"),))
    space_objects = read_space_objects_data_from_file(in_filename)
    max_distance = max([max(abs(obj.x), abs(obj.y)) for obj in space_objects])
    calculate_scale_factor(max_distance)

    for obj in space_objects:
        if obj.type == 'star':
            Star.create_cosmic_body_image(space, obj, scale_x, scale_y)
        elif obj.type == 'planet':
            Planet.create_cosmic_body_image(space, obj, scale_x, scale_y)
        elif obj.type == 'satelite':
            Satelite.create_cosmic_body_image(space, obj, scale_x, scale_y)
        else:
            raise AssertionError("Unknown cosmic body type")


def save_file_dialog():
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    out_filename = asksaveasfilename(filetypes=(("Text file", ".txt"),))
    write_space_objects_data_to_file(out_filename, space_objects)


def main():
    """Главная функция главного модуля.
    Создаёт объекты графического дизайна библиотеки tkinter: окно, холст, фрейм с кнопками, кнопки.
    """
    global physical_time
    global displayed_time
    global time_step
    global time_speed
    global space
    global start_button
    global orbits_button
    global orbit_manager
    #FIXME "1" global entry_x, entry_y 
    print('Modelling started!')
    physical_time = 0

    root = tkinter.Tk()
    root.geometry("+450+50")
    # космическое пространство отображается на холсте типа Canvas
    space = tkinter.Canvas(root, width=window_width, height=window_height, bg="black")
    space.pack(side=tkinter.TOP)
    
    # FIXME "1" space.bind("<Button-3>", handle_right_click) обработчик нажатий 
    
    # управление орбитами
    orbit_manager = OrbitManager(space, scale_x, scale_y, scale_r)
    # нижняя панель с кнопками
    frame = tkinter.Frame(root)
    frame.pack(side=tkinter.BOTTOM)

    orbits_button = Button(frame, text="Show orbits", command=toggle_orbits, width=10)
    orbits_button.pack(side=RIGHT)

    cosmic_bodies_data = tkinter.Button(frame, text="parametrs", command = open_data_window ,width=12)
    cosmic_bodies_data.pack(side=tkinter.LEFT)

    start_button = tkinter.Button(frame, text="Start", command=start_execution, width=6)
    start_button.pack(side=tkinter.LEFT)

    time_step = tkinter.DoubleVar()
    time_step.set(1)
    time_step_entry = tkinter.Entry(frame, textvariable=time_step)
    time_step_entry.pack(side=tkinter.LEFT)

    time_speed = tkinter.DoubleVar()
    scale = tkinter.Scale(frame, variable=time_speed, orient=tkinter.HORIZONTAL)
    scale.pack(side=tkinter.LEFT)

    load_file_button = tkinter.Button(frame, text="Open file...", command=open_file_dialog)
    load_file_button.pack(side=tkinter.LEFT)
    save_file_button = tkinter.Button(frame, text="Save to file...", command=save_file_dialog)
    save_file_button.pack(side=tkinter.LEFT)

    displayed_time = tkinter.StringVar()
    displayed_time.set(str(physical_time) + " seconds gone")
    time_label = tkinter.Label(frame, textvariable=displayed_time, width=30)
    time_label.pack(side=tkinter.RIGHT)

    root.mainloop()
    print('Modelling finished!')


if __name__ == "__main__":
    main()

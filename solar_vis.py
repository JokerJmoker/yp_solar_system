# coding: utf-8
# license: GPLv3

"""Модуль визуализации.
Нигде, кроме этого модуля, не используются экранные координаты объектов.
Функции, создающие гaрафические объекты и перемещающие их на экране, принимают физические координаты
"""
from solar_objects import Orbit
from solar_model import *

header_font = "Arial-16"
"""Шрифт в заголовке"""

window_width = 1000
"""Ширина окна"""

window_height = 800
"""Высота окна"""

scale_factor = None
"""Масштабирование экранных координат по отношению к физическим.
Тип: float
Мера: количество пикселей на один метр."""


def calculate_scale_factor(max_distance):
    """Вычисляет значение глобальной переменной **scale_factor** по данной характерной длине"""
    global scale_factor
    scale_factor = 0.4*min(window_height, window_width)/max_distance
    print('Scale factor:', scale_factor)


"""Возвращает экранную **y(x)** координату по **y(x)** координате модели.
    Принимает вещественное число, возвращает целое число.
    В случае выхода **y(x)** координаты за пределы экрана возвращает
    координату, лежащую за пределами холста.
    Направление оси развёрнуто, чтобы у модели ось **y** смотрела вверх.

    Параметры:

    **y** — y-координата модели.
    """

def scale_x(x):
    return int(x*scale_factor) + window_width//2


def scale_y(y):
    return window_height - int(y * scale_factor)

def scale_r(r):
    return r*scale_factor 

def update_system_name(space, system_name):
    """Создаёт на холсте текст с названием системы небесных тел.
    Если текст уже был, обновляет его содержание.

    Параметры:

    **space** — холст для рисования.
    **system_name** — название системы тел.
    """
    space.create_text(30, 80, tag="header", text=system_name, font=header_font)


def update_object_position(space, body):
    """Перемещает отображаемый объект на холсте.

    Параметры:

    **space** — холст для рисования.
    **body** — тело, которое нужно переместить.
    """
    x = scale_x(body.x)
    y = scale_y(body.y)
    r = body.R
    if x + r < 0 or x - r > window_width or y + r < 0 or y - r > window_height:
        space.coords(body.image, window_width + r, window_height + r,
                     window_width + 2*r, window_height + 2*r)  # положить за пределы окна
    space.coords(body.image, x - r, y - r, x + r, y + r)
    
    
def update_orbit_image(space, space_objects):
    for star_body in space_objects:
        if isinstance(star_body, Star):
            star_ID = star_body.ID
            for planet_body in space_objects:
                if isinstance(planet_body, Planet) and planet_body.ID /11 == star_ID:
                    
                    scaled_star_body_x = scale_x(star_body.x)
                    scaled_star_body_y = scale_y(star_body.y)

                    scaled_planet_orbit_r = scale_r(planet_body.calculate_self_orbit_radius(star_body))
                    planet_orbit_image = space.create_oval(scaled_star_body_x - scaled_planet_orbit_r, scaled_star_body_y - scaled_planet_orbit_r,
                                                            scaled_star_body_x + scaled_planet_orbit_r, scaled_star_body_y + scaled_planet_orbit_r,
                                                            outline="white")
                    space.coords(planet_orbit_image)
                    for satelite_body in space_objects:
                        if isinstance(satelite_body, Satelite) and satelite_body.ID / 11== planet_body.ID:
                            
                            scaled_planet_body_x = scale_x(planet_body.x)
                            scaled_planet_body_y = scale_y(planet_body.y)

                            scaled_satelite_orbit_r = scale_r(satelite_body.calculate_self_orbit_radius(planet_body))
                            satelite_orbit_image = space.create_oval(scaled_planet_body_x - scaled_satelite_orbit_r, scaled_planet_body_y - scaled_satelite_orbit_r,
                                                                    scaled_planet_body_x + scaled_satelite_orbit_r, scaled_planet_body_y + scaled_satelite_orbit_r,
                                                                    outline="white")
                            space.coords(satelite_orbit_image)


   
    

if __name__ == "__main__":
    print("This module is not for direct call!")

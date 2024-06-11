# coding: utf-8
# license: GPLv3

from solar_objects import *
G = 6.67408E-11
"""Гравитационная постоянная Ньютона G"""


def recalculate_space_objects_positions(space_objects, dt):
    """Пересчитывает координаты объектов.

    Параметры:

    **space_objects** — список объектов, для которых нужно пересчитать координаты.
    **dt** — шаг по времени
    """

    for center_body in space_objects:
        if isinstance(center_body, Star):
            for satellite_body in space_objects:
                if isinstance(satellite_body, Satelite):
                    satellite_body.rotate_around(center_body, dt)


if __name__ == "__main__":
    print("This module is not for direct call!")

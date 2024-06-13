# coding: utf-8
# license: GPLv3

from solar_objects import *

def recalculate_space_objects_positions(space_objects, dt):
    """Пересчитывает координаты объектов.

    Параметры:

    **space_objects** — список объектов, для которых нужно пересчитать координаты.
    **dt** — шаг по времени
    
    star_body - это centre_body, вокруг готорого вращается planet и т.д
    """
    
    for star_body in space_objects:
        if isinstance(star_body, Star):
            star_ID_for_static = star_body.ID_for_static
            for planet_body in space_objects:
                if isinstance(planet_body, Planet) and planet_body.ID_for_static /11 == star_ID_for_static:
                    planet_body.rotate_planet_around(star_body, dt)
                    planet_ID_for_staic = planet_body.ID_for_static
                    planet_ID_for_rotating = planet_body.ID_for_rotating
                    for satelite_body in space_objects:
                        if isinstance(satelite_body, Satelite) and satelite_body.ID_for_static / 11 == planet_ID_for_staic and satelite_body.ID_for_rotating == planet_ID_for_rotating:
                            satelite_body.rotate_satelite_around(planet_body, dt)
                            
                            
if __name__ == "__main__":
    print("This module is not for direct call!")

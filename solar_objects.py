# coding: utf-8
# license: GPLv3


class CosmicBody:
    """Тип данных, описывающий звезду.
    Содержит массу, координаты, скорость звезды,
    а также визуальный радиус звезды в пикселах и её цвет.
    """
    type : str
    """Признак объекта звезды"""
    R : int
    """Радиус звезды"""
    color : str
    """Цвет звезды"""
    x : float
    """Координата по оси **x**"""
    y : float
    """Координата по оси **y**"""
    ID_for_static: int
    """Идентификатор тела"""
    image = None
    """Изображение звезды"""
    

    def parse_cosmic_body_parameters(self, line):
        """Считывает данные о звезде из строки.
        
        Входная строка должна иметь следующий формат:
        Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>
        
        Здесь (x, y) — координаты планеты, (Vx, Vy) — скорость.
        Пример строки:
        Star 50 yellow 1.0 100.0 200.0 0.0 0.0
        
        Параметры:
        **line** — строка с описанием звезды.
        **star** — объект звезды.
        """
        line = line.strip()
        if line and not line.startswith('#'):
            parts = line.split()
            
            self.R = int(parts[1])
            self.color = parts[2]
            self.x = float(parts[3])
            self.y = float(parts[4])
            self.ID_for_static = int(parts[-1])


    @staticmethod
    def create_cosmic_body_image(space,obj,scale_x,scale_y):
        """Создаёт отображаемый объект.

        Параметры:

        **space** — холст для рисования.
        **star** — объект звезды.
        """
        x = scale_x(obj.x)
        y = scale_y(obj.y)
        r = obj.R
        obj.image = space.create_oval([x - r, y - r], [x + r, y + r], fill=obj.color)


class Star(CosmicBody):    
    type = 'star'


    def parse_star_parameters(self, line):
        super().parse_cosmic_body_parameters(line)


class Planet(CosmicBody):
    type = 'planet'

    V_tg : float
    """Тангенцальная скорсоть"""

    ID_for_rotating : int 


    def parse_planet_parameters(self, line):
        super().parse_cosmic_body_parameters(line)

        line = line.strip()
        if line and not line.startswith('#'):
            parts = line.split()
            
            self.V_tg = float(parts[5])
            self.ID_for_rotating = int(parts[-2])
            

    def rotate_planet_around(self, center_body, dt):
        import math
        """Вращает тело вокруг другого тела.

        Параметры:
        - center_body: Тело, вокруг которого нужно вращаться.
        - dt: Временной шаг.
        """
        r = ((self.x - center_body.x)**2 + (self.y - center_body.y)**2)**0.5
        if r == 0:
            return
        omega = self.V_tg / r
        phi = omega * dt
        new_x = (self.x - center_body.x) * math.cos(phi) - (self.y - center_body.y) * math.sin(phi) + center_body.x
        new_y = (self.x - center_body.x) * math.sin(phi) + (self.y - center_body.y) * math.cos(phi) + center_body.y
        self.x = new_x
        self.y = new_y


    def calculate_self_orbit_radius(self, center_body):
        orbit_r = ((self.x - center_body.x) ** 2 + (self.y - center_body.y) ** 2) ** 0.5
        return orbit_r
        
    
class Satelite(Planet):
    type = 'satelite'


    def parse_satelite_parameters(self, line):
        super().parse_planet_parameters(line)
    
      
    def rotate_satelite_around(self, center_body, dt):
        import math
        r = ((self.x - center_body.x)**2 + (self.y - center_body.y)**2)**0.5
        if r == 0:
            return
        V_tg = self.V_tg + center_body.V_tg 
        omega = (V_tg)/ r
        phi = omega * dt
        new_x = (self.x - center_body.x) * math.cos(phi) - (self.y - center_body.y) * math.sin(phi) + center_body.x
        new_y = (self.x - center_body.x) * math.sin(phi) + (self.y - center_body.y) * math.cos(phi) + center_body.y
        self.x = new_x
        self.y = new_y  


class OrbitManager:
    def __init__(self, space, scale_x, scale_y, scale_r):
        self.space = space
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.scale_r = scale_r
        self.orbit_images = []


    def create_orbit(self, center_body, orbiting_body, outline_color="white"):
        scaled_center_x = self.scale_x(center_body.x)
        scaled_center_y = self.scale_y(center_body.y)
        scaled_orbit_r = self.scale_r(orbiting_body.calculate_self_orbit_radius(center_body))
        
        orbit_image = self.space.create_oval(scaled_center_x - scaled_orbit_r, scaled_center_y - scaled_orbit_r,
                                             scaled_center_x + scaled_orbit_r, scaled_center_y + scaled_orbit_r,
                                             outline=outline_color)
        self.orbit_images.append(orbit_image)


    def update_orbit_images(self, space_objects):
        self.clear_orbit_images()
        for star_body in space_objects:
            if isinstance(star_body, Star):
                for planet_body in space_objects:
                    if isinstance(planet_body, Planet) and planet_body.ID_for_static // 11 == star_body.ID_for_static:
                        self.create_orbit(star_body, planet_body)
                        for satellite_body in space_objects:
                            if isinstance(satellite_body, Satelite) and satellite_body.ID_for_static // 11 == planet_body.ID_for_static and satellite_body.ID_for_rotating == planet_body.ID_for_rotating:
                                self.create_orbit(planet_body, satellite_body)


    def clear_orbit_images(self):
        for image in self.orbit_images:
            self.space.delete(image)
        self.orbit_images = []

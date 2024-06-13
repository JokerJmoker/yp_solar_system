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
    ID: int
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
            self.ID = int(parts[-1])

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


    def parse_planet_parameters(self, line):
        super().parse_cosmic_body_parameters(line)

        line = line.strip()
        if line and not line.startswith('#'):
            parts = line.split()
            
            self.V_tg = float(parts[5])
            

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
        
class Orbit:
   

    @staticmethod
    def calculate_orbit_radius(space_objects):
        """Create orbit path images for planets and satellites around stars."""
        for rotating_bodie in space_objects:
            if isinstance(rotating_bodie, Planet) or isinstance(rotating_bodie, Satelite):
                for center_body in space_objects:
                    if isinstance(center_body, Star):
                        orbit_r = ((rotating_bodie.x - center_body.x) ** 2 + (rotating_bodie.y - center_body.y) ** 2) ** 0.5
                        #rotating_bodie.orbit_image = space.create_oval(center_body.x - orbit_r, center_body.y - orbit_r,
                        #                                    center_body.x + orbit_r, center_body.y + orbit_r,
                        #                                    outline="white")

    @staticmethod
    def clear_orbit_images(space_objects, space):
        """Clear orbit path images from the canvas."""
        for obj in space_objects:
            if isinstance(obj, Planet) or isinstance(obj, Satelite):
                if hasattr(obj, 'orbit_image') and obj.orbit_image:
                    space.delete(obj.orbit_image)
                    obj.orbit_image = None

    @staticmethod
    def update_orbit_positions(space_objects, scale_x, scale_y, scale_r, space):
        """Update positions of orbit path images on the canvas."""
        for rotating_body in space_objects:
            if isinstance(rotating_body, Planet) or isinstance(rotating_body, Satelite):
                for center_body in space_objects:
                    if isinstance(center_body, Star):
                        r = ((rotating_body.x - center_body.x) ** 2 + (rotating_body.y - center_body.y) ** 2) ** 0.5
                        scaled_r = scale_r(r)
                        center_x = scale_x(center_body.x)
                        center_y = scale_y(center_body.y)
                        space.coords(rotating_body.orbit_image, center_x - scaled_r, center_y - scaled_r,
                                    center_x + scaled_r, center_y + scaled_r)

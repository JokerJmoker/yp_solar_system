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
    m : float
    """Масса звезды"""
    x : float
    """Координата по оси **x**"""
    y : float
    """Координата по оси **y**"""

    Fx : float
    """Сила по оси **x**"""
    Fy : float
    """Сила по оси **y**"""
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
            self.m = float(parts[3])
            self.x = float(parts[4])
            self.y = float(parts[5])


    @staticmethod
    def create_cosmic_body_image(space,obj,scale_x,scale_y):
        """Создаёт отображаемый объект звезды.

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


class Satelite(CosmicBody):

    type = 'planet'

    Vx : float
    """Скорость по оси **x**"""
    Vy : float
    """Скорость по оси **y**"""


    def parse_planet_parameters(self, line):
        super().parse_cosmic_body_parameters(line)

        line = line.strip()
        if line and not line.startswith('#'):
            parts = line.split()
            
            self.Vx = float(parts[6])
            self.Vy = float(parts[7])

    
    def define_tangential_velocity(self):
        """Вычисляет тангенциальную скорость планеты.

        Возвращает:
        - tangential_velocity: Тангенциальная скорость планеты.
        """
        tangential_velocity = (self.Vx**2 + self.Vy**2)**0.5
        return tangential_velocity

    def rotate_around(self, center_body, dt):
        import math
        """Вращает тело вокруг другого тела.

        Параметры:
        - center_body: Тело, вокруг которого нужно вращаться.
        - dt: Временной шаг.
        """
        tangential_velocity = self.define_tangential_velocity()
        
        # Расстояние между телами
        radius = ((self.x - center_body.x)**2 + (self.y - center_body.y)**2)**0.5
        
        # Угловая скорость
        angular_velocity = tangential_velocity / radius
        
        # Угол изменения
        angle_change = angular_velocity * dt
        
        # Пересчет координат
        new_x = (self.x - center_body.x) * math.cos(angle_change) - (self.y - center_body.y) * math.sin(angle_change) + center_body.x
        new_y = (self.x - center_body.x) * math.sin(angle_change) + (self.y - center_body.y) * math.cos(angle_change) + center_body.y
        
        # Установка новых координат
        self.x = new_x
        self.y = new_y
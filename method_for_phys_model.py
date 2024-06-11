# здесь указаны методы при наличии сил

def calculate_cosmic_body_force(self, space_objects, G):
        import math
        """Вычисляет силу, действующую на тело.

        Параметры:

        **body** — тело, для которого нужно вычислить дейстующую силу.
        **space_objects** — список объектов, которые воздействуют на тело.
        """

        self.Fx = self.Fy = 0
        for obj in space_objects:
            if self == obj:
                continue  # тело не действует гравитационной силой на само себя!
            r = ((self.x - obj.x)**2 + (self.y - obj.y)**2)**0.5
            F = G*((self.m*obj.m)/r**2)  # FIXME: нужно вывести формулу...
            alpha = math.atan2(obj.y - self.y, obj.x - self.x)
            self.Fx += F * math.cos(alpha)
            self.Fy += F * math.sin(alpha)

def move_cosmic_body(self, dt):
        """Перемещает тело в соответствии с действующей на него силой.

        Параметры:

        **body** — тело, которое нужно переместить.
        """

        ax = self.Fx/self.m
        self.Vx += ax*dt # учтена v0 при +=
        self.x += self.Vx*dt + (ax*dt**2)/2 # учтено x0 при +=
        # FIXME: not done recalculation of y coordinate!
        ay = self.Fy/self.m
        self.Vy += ay*dt
        self.y += self.Vy*dt + (ay*dt**2)/2 
        
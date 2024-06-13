def create_orbit_images():
    for obj in space_objects:
        if isinstance(obj, Planet) or isinstance(obj, Satelite):
            for star in space_objects:
                if isinstance(star, Star):
                    r = ((obj.x - star.x) ** 2 + (obj.y - star.y) ** 2) ** 0.5
                    scaled_r = r * scale_factor
                    center_x = scale_x(star.x)
                    center_y = scale_y(star.y)
                    obj.orbit_image = space.create_oval(center_x - scaled_r, center_y - scaled_r,
                                                         center_x + scaled_r, center_y + scaled_r,
                                                         outline="white")

def clear_orbit_images():
    for obj in space_objects:
        if isinstance(obj, Planet) or isinstance(obj, Satelite):
            if obj.orbit_image:
                space.delete(obj.orbit_image)
                obj.orbit_image = None

def update_orbit_positions():
    for obj in space_objects:
        if isinstance(obj, Planet) or isinstance(obj, Satelite):
            for star in space_objects:
                if isinstance(star, Star):
                    r = ((obj.x - star.x) ** 2 + (obj.y - star.y) ** 2) ** 0.5
                    scaled_r = r * scale_factor
                    center_x = scale_x(star.x)
                    center_y = scale_y(star.y)
                    space.coords(obj.orbit_image, center_x - scaled_r, center_y - scaled_r,
                                 center_x + scaled_r, center_y + scaled_r)

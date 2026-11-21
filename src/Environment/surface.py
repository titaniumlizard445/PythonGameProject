#Surface handler (kinda like a blueprint for the renderer)

import pygame

class Surface:

    def __init__(self, x, y, z, w, h, d, own, obj_type, color):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.h = h
        self.d = d
        self.own = own
        self.obj_type = obj_type
        self.color = color


    def get_bounds(self):
        return ((self.x, self.x+self.w), (self.y - self.d, self.y), (self.z, self.z + self.h))


    def get_corners(self):
        return ((self.x, self.y, self.z + self.h), (self.x + self.w, self.y, self.z + self.h), (self.x + self.w, self.y, self.z), (self.x, self.y, self.z))


    def get_scrn_corners(self):
        corners = self.get_corners()
        scrn_corners = []

        for corner in corners:
            scrn_corners.append((corner[0],corner[1] - corner[2]))

        return scrn_corners


    def get_scrn_bounds(self):
        corners = self.get_scrn_corners()
        x_vals = []
        y_vals = []

        for corner in corners:
            x_vals.append(corner[0])
            y_vals.append(corner[1])

        return ((min(x_vals), max(x_vals)), (min(y_vals), max(y_vals)))


    def draw(self, screen):
        corners = self.get_scrn_corners()

        pygame.draw.polygon(screen, self.color, corners, 0)

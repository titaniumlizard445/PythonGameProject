#Environmental Slope class

import pygame

class Slope:

    def __init__(self, x, y, z, w, h, d, direction=1):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.h = h
        self.d = d
        self.direction = direction


    def get_height_at(self, x):
        return (((x - self.x) / self.w) * self.h * self.direction) + self.z


    def contains_x(self, x):
        if x >= self.x and x <= self.x + self.w:
            return True

        return False


    def contains_y(self, y):
        if y <= self.y and y >= self.y - self.d:
            return True

        return False


    def overlaps_player(self, player):
        x_overlap = (min(self.x + self.w, player.x + player.width) - max(self.x, player.x))

        y_overlap = (min(self.y, player.y) - max(self.y - self.d, player.y - player.depth))

        return x_overlap > 0 and y_overlap > 0


    def get_player_surface_height(self, player):
        player_mid_x = player.x + player.width / 2
        return self.get_height_at(player_mid_x)


    def draw(self, screen, camera_x=0):
        dep_points = ((self.x - camera_x, self.y - self.z), (self.x + self.w - camera_x, self.y - (self.z + self.h * self.direction)),  (self.x + self.w - camera_x, self.y - self.d - (self.z + self.h * self.direction)), (self.x - camera_x, self.y - self.d - self.z))
        bottom_z = 0
        front_points = ((self.x - camera_x, self.y - self.z), (self.x + self.w - camera_x, self.y - (self.z + self.h * self.direction)), (self.x + self.w -camera_x, self.y - bottom_z), (self.x - camera_x, self.y - bottom_z))
        pygame.draw.polygon(screen, (100, 15, 100), dep_points, 0)
        pygame.draw.polygon(screen, (70, 10, 70), front_points, 0)


    @property
    def gradient(self):
        return abs(self.h / self.w)
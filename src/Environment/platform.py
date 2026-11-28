#platform handler
import pygame

class Platform:

    def __init__(self , x, y, z, width, height, depth):
        self.x = x
        self.y = y
        self.z = z
        self.depth = depth
        self.width = width
        self.height = height
        self.color = (30, 50, 20)


    def draw(self, screen, camera_x=0):
        vertical_pos = self.y - self.z
        pygame.draw.polygon(screen, self.color, [(self.x - camera_x, vertical_pos), (self.x +self.width - camera_x, vertical_pos), (self.x +self.width - camera_x,vertical_pos - self.depth), (self.x - camera_x, vertical_pos - self.depth)], 0)

    @property
    def depth_sort(self):
        return self.y - self.depth / 2


    @property
    def front_depth(self):
        return self.y


    @property
    def back_depth(self):
        return self.y - self.depth
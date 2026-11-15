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
        self.color = (100, 50, 20)
        self.top_color = (100, 100, 100)

    
    def draw(self,screen):
        vertical_pos = self.y - self.z
        pygame.draw.polygon(screen, self.top_color, [(self.x, vertical_pos), (self.x +self.width, vertical_pos), (self.x +self.width - self.depth ,vertical_pos - self.depth), (self.x - self.depth, vertical_pos - self.depth)], 0)


    def draw_top(self, screen):
        vertical_pos = self.y - self.z
        pygame.draw.polygon(screen, self.top_color, [(self.x, vertical_pos), (self.x +self.width, vertical_pos), (self.x +self.width - self.depth ,vertical_pos - self.depth), (self.x - self.depth, vertical_pos - self.depth)], 0)

    @property
    def depth_sort(self):
        return self.y - self.depth / 2


    @property
    def front_depth(self):
        return self.y


    @property
    def back_depth(self):
        return self.y - self.depth
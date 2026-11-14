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
        pygame.draw.rect(screen, self.color, (self.x, self.z, self.width, self.height))
        #draw 3D part
        pygame.draw.polygon(screen, self.top_color, [(self.x, self.z), (self.x +self.width, self.z), (self.x +self.width - 50 ,self.z - self.depth), (self.x - 50, self.z - self.depth)], 0)
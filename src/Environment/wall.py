#wall handler

import pygame
from src.Environment.surface import Surface

class Wall:

    def __init__(self, x, y, z, width, height, depth):
        #physical confines  !IMPORTANT! Z IS THE BOTTOM OF THE WALL
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.height = height
        self.depth = depth

        self.color = (120, 10, 20)


    def draw_front(self, screen):
        vertical_pos = self.y - self.z - self.height
        pygame.draw.rect(screen, self.color, (self.x, vertical_pos, self.width, self.height))
        

    def get_front_surface(self):
        return Surface(self.x, self.y, self.z, self.width, self.height, 0, self, "wall_front", self.color)

        
    def overlap_xy(self, player):
        #check x and y overlap
        if 0 < (min(self.x + self.width, player.x + player.width) - max(self.x, player.x)):
            if player.y > self.y - self.depth and player.y - player.depth < self.y:
                return True

        return False

    
    def overlap_z(self, player):
        #check z
        if self.z < player.z + player.height and player.z < self.z + self.height:
            return True

        return False


    def check_col(self, player):
        if self.overlap_xy(player):
            if self.overlap_z(player):
                return True

        return False


    @property
    def front_depth(self):
        return self.y


#wall handler

import pygame

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

    
    def draw(self,screen):
        vertical_pos = self.y - self.z - self.height
        pygame.draw.rect(screen, self.color, (self.x, vertical_pos, self.width, self.height))
        #3D look
        pygame.draw.polygon(screen,(50, 50, 50), [(self.x, vertical_pos), (self.x, vertical_pos + self.height), (self.x - self.depth, vertical_pos + self.height - self.depth), (self.x - self.depth, vertical_pos - self.depth)], 0)
        #debugging
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.width, self.depth), 2)
        pygame.draw.line(screen, (255, 255, 0), (self.x, self.y - self.z), (self.x + self.width, self.y - self.z), 2)

    def overlap_xy(self, player):
        #check x and y overlap
        if 0 < (min(self.x + self.width, player.x + player.width) - max(self.x, player.x)):
            if 0 < min(self.y + self.depth, player.y + player.depth) - max(self.y, player.y):
                return True

        return False

    
    def overlap_z(self, player):
        #check z
        if self.z <= player.z + player.height and player.z <= self.z + self.height:
            return True

        return False


    def check_col(self, player):
        if self.overlap_xy(player):
            print("X and Y overlap")
            if self.overlap_z(player):
                print("FULL COLLISION")
                return True

        return False
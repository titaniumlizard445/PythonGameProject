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


    def draw_side(self, screen):
        vertical_pos = self.y - self.z - self.height
        pygame.draw.polygon(screen,(50, 50, 50),((self.x, vertical_pos), (self.x, vertical_pos + self.height), (self.x - self.depth, vertical_pos + self.height - self.depth), (self.x - self.depth, vertical_pos - self.depth)), 0)
    

    def draw_front(self, screen):
        vertical_pos = self.y - self.z - self.height
        pygame.draw.rect(screen, self.color, (self.x, vertical_pos, self.width, self.height))
        
        
        
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


    def covers_player(self, player):
        # Player must overlap the wall horizontally
        x_overlap = (player.x < self.x + self.width and player.x + player.width > self.x - self.depth)

        # Player must be completely behind the wall in depth
        behind_wall = player.y < self.y - self.depth

        # Player must be standing, not jumping
        grounded = player.is_grounded

        # Player and wall must occupy overlapping vertical space
        vertical_overlap = (player.z < self.z + self.height and player.z + player.height > self.z)

        return (x_overlap and behind_wall and grounded and vertical_overlap)


    def covers_shadow(self, player, platforms):
        # Include the front and projected side of the wall
        x_overlap = (player.x < self.x + self.width and player.x + player.width > self.x - self.depth)

        # Shadow must be completely behind the wall
        behind_wall = player.y < self.y - self.depth

        # Find the height of the shadow
        shadow_z = player.get_shadow_height(platforms)

        # Shadow must be below the top of the wall
        vertical_overlap = (self.z <= shadow_z < self.z + self.height)

        return x_overlap and behind_wall and vertical_overlap


    @property
    def front_depth(self):
        return self.y

    
    @property
    def side_depth(self):
        return self.y - self.depth / 2


    @property
    def back_depth(self):
        return self.y - self.depth
    
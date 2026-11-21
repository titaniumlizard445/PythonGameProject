#contains basic enemy information

import pygame

class Enemy:

    def __init__(self, x, y, z=0):
        #position
        self.x = x
        self.y = y
        self.z = z

        #size
        self.width = 50
        self.height = 80
        self.depth = 40

        #stats
        self.health = 100
        self.max_health = 100
        self.alive = True
        self.color = (0, 250, 100)

        #combat
        self.been_hit = False
        self.invuln_t = 0.0
        self.invuln_dur = 0.25


    def get_screen_coords(self):
        screen_x = self.x 
        screen_y = self.y - self.z - self.height
    
        return screen_x, screen_y


    def draw(self, screen):
        scn_x, scn_y = self.get_screen_coords()
        pygame.draw.rect(screen, self.color, (scn_x, scn_y, self.width, self.height))


    @property
    def depth_sort(self):
        return self.y - self.depth / 2


    @property
    def sort_z(self):
        return self.z + self.height / 2


    @property
    def sort_value(self):
        return self.depth_sort + (self.sort_z * 0.5)


    def check_col(self, incoming_hitbox):
        atk_x, atk_y, atk_z, atk_w, atk_h, atk_d = incoming_hitbox
        if self.x + self.width >= atk_x  and self.x  <= atk_x + atk_w:
            if self.y >= atk_y - atk_d and self.y - self.depth <= atk_y:
                if self.z + self.height >= atk_z  and self.z  <= atk_z + atk_h:
                    return True

        return False


    def update(self, dt):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.been_hit = False

        if self.invuln_t > 0:
            self.invuln_t = max( 0, self.invuln_t - dt)
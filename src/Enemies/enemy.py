#contains basic enemy information

import pygame

class Enemy:

    def __init__(self, x, y, z=0):
        #position
        self.x = x
        self.y = y
        self.z = z

        #movement
        self.x_speed = 150
        self.y_speed = 100

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
        self.attack_range = 60
        self.windup_duration = 0.4
        self.active_duration = 0.15
        self.recovery_duration = 0.5
        self.attack_direction = 1
        self.attack_cooldown = 0.0
        self.attack_cooldown_duration = 0.8

        #attack dimensions
        self.punch_w = 70
        self.punch_h = 40
        self.punch_d = 50

        #AI
        self.awareness_range = 250
        self.player_detected = False
        self.state = "idle"
        self.current_attack = "basic_punch"
        self.attack_phase = ""
        self.attack_timer = 0.0
        self.attack_target_y = 0


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


    def update(self, dt, player):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.been_hit = False

        if not self.alive:
            return

        if self.invuln_t > 0:
            self.invuln_t = max(0, self.invuln_t - dt)

        if self.attack_cooldown > 0:
            self.attack_cooldown = max(0, self.attack_cooldown - dt)

        self.detect_player(player)

        if self.state == "attacking":
            self.update_attack(dt)

        else:
            if self.player_detected:
                if self.in_attack_range(player) and self.attack_cooldown <= 0:
                    if self.state != "attacking":
                        self.state = "attacking"
                        self.attack_phase = "windup"
                        self.attack_timer = 0
                        self.attack_target_y = player.y - player.depth / 2

                        e_center_x = self.x + self.width / 2
                        p_center_x = player.x + player.width / 2
                        if p_center_x > e_center_x:
                            self.attack_direction = 1
                        else:
                            self.attack_direction = -1

                else:
                    self.state = "chasing"
            else:
                self.state = "idle"

            if self.state == "chasing":
                self.pursue(player, dt)


    def detect_player(self, player):
        e_cntr_x = self.x + self.width / 2
        e_cntr_y = self.y - self.depth / 2
        p_cntr_x = player.x + player.width /2
        p_cntr_y = player.y - player.depth / 2

        self.player_detected = False

        if abs(e_cntr_x - p_cntr_x) <= self.awareness_range:
            if abs(e_cntr_y - p_cntr_y) <= self.awareness_range:
                self.player_detected = True


    def pursue(self, player, dt):
        e_cntr_x = self.x + self.width / 2
        e_cntr_y = self.y - self.depth / 2
        p_cntr_x = player.x + player.width /2
        p_cntr_y = player.y - player.depth / 2

        dx = abs(p_cntr_x - e_cntr_x)
        dy = abs(p_cntr_y - e_cntr_y)

        if dx > self.attack_range:
            if p_cntr_x > e_cntr_x:
                self.x  += min(dx - self.attack_range, self.x_speed * dt)
            elif p_cntr_x < e_cntr_x:
                self.x  -= min(dx - self.attack_range, self.x_speed * dt)

        if dy > self.attack_range:
            if p_cntr_y > e_cntr_y:
                self.y  += min(dy - self.attack_range, self.y_speed * dt)
            elif p_cntr_y < e_cntr_y:
                self.y -= min(dy - self.attack_range, self.y_speed * dt)


    def in_attack_range(self, player):
        e_cntr_x = self.x + self.width / 2
        e_cntr_y = self.y - self.depth / 2
        p_cntr_x = player.x + player.width / 2
        p_cntr_y = player.y - player.depth / 2
        dx = abs(p_cntr_x - e_cntr_x)
        dy = abs(p_cntr_y - e_cntr_y)

        if dx <= self.attack_range and dy <= self.attack_range:
            return True
        else:
            return False


    def update_attack(self, dt):
        self.attack_timer += dt

        if self.attack_phase == "windup":
            if self.attack_timer >= self.windup_duration:
                self.attack_phase = "active"
                self.attack_timer = 0

        elif self.attack_phase == "active":
            if self.attack_timer >= self.active_duration:
                self.attack_phase = "recovery"
                self.attack_timer = 0

        elif self.attack_phase == "recovery":
            if self.attack_timer >= self.recovery_duration:
                self.attack_phase = ""
                self.attack_timer = 0
                self.attack_cooldown = self.attack_cooldown_duration
                self.state = "chasing"


    def get_attack_hitbox(self):
        if self.attack_phase == "active":
            atk_y = self.attack_target_y + (self.punch_d/2)
    
            if self.attack_direction == -1:
                punch_x = self.x - self.punch_w
            elif self.attack_direction == 1:
                punch_x = self.x + self.width
    
            hitbox = (punch_x, atk_y, self.z, self.punch_w, self.punch_h, self.punch_d)
    
            #hitbox = tuple (xpos, ypos, jab width, jab height, jab depth)
            return hitbox
            
        else:
            return None


    #Temporary hitbox debugging tool
    def draw_attack_hitbox(self, screen):
        hitbox = self.get_attack_hitbox()

        if hitbox is not None:
            x, y, z, w, h, d = hitbox

            # Convert world coordinates to screen coordinates
            screen_x = x
            screen_y = y - z - h

            # Draw a transparent red rectangle
            debug_surface = pygame.Surface((w, h), pygame.SRCALPHA)
            debug_surface.fill((255, 0, 0, 100))

            screen.blit(debug_surface, (screen_x, screen_y))

            # Draw the outline
            pygame.draw.rect(screen, (255, 0, 0), (screen_x, screen_y, w, h), 2)
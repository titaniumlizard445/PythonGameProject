#contains basic enemy information

import pygame
import random

class Enemy:

    def __init__(self, x, y, z=0):
        #position
        self.x = x
        self.y = y
        self.z = z
        self.direction = 1

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
        self.attack_range = 70
        self.attacks = {
            "basic punch": {
                "windup": 0.4,
                "active": 0.15,
                "recovery": 0.5,
                "cooldown": 0.8,
                "damage": 25,
                "width": 70,
                "height": 40,
                "depth": 50,
                "lunge": 0,
                "lunge speed": 0
            },
            "heavy punch": {
                "windup": 0.7,
                "active": 0.25,
                "recovery": 0.8,
                "cooldown": 1.3,
                "damage": 40,
                "width": 100,
                "height": 65,
                "depth": 65,
                "lunge": 45,
                "lunge speed": 180
            }
        }
        self.windup_duration = 0.4
        self.active_duration = 0.15
        self.recovery_duration = 0.5
        self.attack_direction = 1
        self.attack_cooldown = 0.0
        self.attack_cooldown_duration = 0
        self.attack_damage = 0
        self.lunge = 0
        self.lunge_speed = 0
        self.lunge_dist = 0

        #attack dimensions
        self.atk_w = 70
        self.atk_h = 40
        self.atk_d = 50

        #AI
        self.awareness_range = 250
        self.player_detected = False
        self.state = "idle"
        self.current_attack = "basic punch"
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
        side = self.attack_range * self.direction
        pygame.draw.line(screen, (250, 50, 0), (self.x + self.width / 2, self.y - self.z - (self.height * 3) /4), (self.x + self.width / 2 + side, self.y - self.z - (self.height * 3) /4), 4)


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


    def update(self, dt, player, walls, enemies):
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
            self.update_attack(dt, walls, player, enemies)

        else:
            self.combat_checks(player, dt, walls, enemies)
            


    def combat_checks(self, player, dt, walls, enemies):
        if self.player_detected:
            if self.in_attack_range(player) and self.attack_cooldown <= 0:
                if self.state != "attacking":
                    self.state = "attacking"
                    self.attack_phase = "windup"
                    self.attack_timer = 0
                    self.attack_target_y = player.y - player.depth / 2
        
                    #choose an attack
                    self.current_attack = random.choice(list(self.attacks.keys()))
                    atk_data = self.attacks[self.current_attack]
        
                    #assign data
                    self.attack_damage = atk_data["damage"]
                    self.lunge = atk_data["lunge"]
                    self.lunge_speed = atk_data["lunge speed"]
                    self.lunge_dist = 0
                    self.windup_duration = atk_data["windup"]
                    self.active_duration = atk_data["active"]
                    self.recovery_duration = atk_data["recovery"]
        
                    self.atk_w = atk_data["width"]
                    self.atk_h = atk_data["height"]
                    self.atk_d = atk_data["depth"]
                    self.attack_cooldown_duration = atk_data["cooldown"]
                                
        
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
            self.pursue(player, dt, walls, enemies)

    def detect_player(self, player):
        e_cntr_x = self.x + self.width / 2
        e_cntr_y = self.y - self.depth / 2
        p_cntr_x = player.x + player.width /2
        p_cntr_y = player.y - player.depth / 2

        self.player_detected = False

        if abs(e_cntr_x - p_cntr_x) <= self.awareness_range:
            if abs(e_cntr_y - p_cntr_y) <= self.awareness_range:
                self.player_detected = True


    def pursue(self, player, dt, walls, enemies):
        e_cntr_x = self.x + self.width / 2
        e_cntr_y = self.y - self.depth / 2
        p_cntr_x = player.x + player.width /2
        p_cntr_y = player.y - player.depth / 2

        if p_cntr_x - e_cntr_x < 0:
            self.direction = -1
        else:
            self.direction = 1

        dx = abs(p_cntr_x - e_cntr_x)
        dy = abs(p_cntr_y - e_cntr_y)

        if dx > self.attack_range:
            move_x = min(dx - self.attack_range, self.x_speed * dt)

            if p_cntr_x < e_cntr_x:
                move_x *= -1

            self.wall_restricted_x(move_x, walls, player, enemies)

        if dy > self.attack_range:
            move_y = min(dy - self.attack_range, self.y_speed * dt)

            if p_cntr_y < e_cntr_y:
                move_y *= -1

            self.wall_restricted_y(move_y, walls, player, enemies)
            


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


    def update_attack(self, dt, walls, player, enemies):
        self.attack_timer += dt


        if self.attack_phase == "windup":
            remaining = max(0, self.lunge - self.lunge_dist)
            move = min(remaining, self.lunge_speed * dt)

            if self.attack_direction == 1:
                move *= 1
            else:
                move *= -1

            displacement = self.wall_restricted_x(move, walls, player, enemies)

            self.lunge_dist += abs(displacement)
            
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
            atk_y = self.attack_target_y + (self.atk_d/2)
    
            if self.attack_direction == -1:
                punch_x = self.x - self.atk_w
            elif self.attack_direction == 1:
                punch_x = self.x + self.width
    
            hitbox = (punch_x, atk_y, self.z, self.atk_w, self.atk_h, self.atk_d)
    
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


    def wall_restricted_x(self, movement, walls, player, enemies):
        previous_x = self.x
        self.x += movement

        for wall in walls:
            if wall.check_col(self):
                self.x = previous_x
                break

        if self.check_body_collision(player):
            self.x = previous_x

        for enemy in enemies:
            if enemy.alive and self.check_body_collision(enemy):
                self.x = previous_x
                break
        
        return self.x - previous_x


    def wall_restricted_y(self, movement, walls, player, enemies):
        previous_y = self.y
        self.y += movement

        for wall in walls:
            if wall.check_col(self):
                self.y = previous_y
                break

        if self.check_body_collision(player):
            self.y = previous_y

        for enemy in enemies:
            if enemy.alive and self.check_body_collision(enemy):
                self.y = previous_y
                break


    def check_body_collision(self, other):
        # X overlap
        if self.x + self.width <= other.x or self.x >= other.x + other.width:
            return False

        # Y overlap
        if self.y <= other.y - other.depth or self.y - self.depth >= other.y:
            return False

        # Z overlap
        if self.z + self.height <= other.z or self.z >= other.z + other.height:
            return False

        return True
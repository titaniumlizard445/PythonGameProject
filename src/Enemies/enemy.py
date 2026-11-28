#contains basic enemy information

import pygame
import random
import math

class Enemy:

    def __init__(self, e_type, x, y, behavior="normal", z=0, boss=False):
        #position
        self.x = x
        self.y = y
        self.z = z
        self.direction = 1

        self.enemy_types = {
            "basic":{
                "x_speed": 150,
                "y_speed": 100,
                "max_x_vel": 300,
                "width": 50,
                "height": 80,
                "depth": 40,
                "health": 100,
                "max_health": 100,
                "color": (0, 250, 100), #colors are temporary for visual testing
                "attack_range": 70,
                "position_style": "balanced",
                "reposition_distance": 150,
                "reposition_delay": 0.5,
                "break_threshold": 4,
                "attacks":{
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
                        "lunge speed": 0,
                        "charge speed": 0,
                        "weight": 2,
                        "indicator color": (255, 200, 0),
                        "indicator size": 8
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
                        "lunge speed": 180,
                        "charge speed": 0,
                        "weight": 2,
                        "indicator color": (255, 120, 0),
                        "indicator size": 14
                    },
                    "charge":{
                        "windup": 0.8,
                        "active": 0.6,
                        "recovery": 1.0,
                        "cooldown": 2.0,
                        "damage": 30,
                        "width": 0,
                        "height": 80,
                        "depth": 50,
                        "lunge": 0,
                        "lunge speed": 0,
                        "charge speed": 250,
                        "weight": 1,
                        "indicator color": (255, 40, 40),
                        "indicator size": 16
                    }
                }
            },
            "heavy":{
                "x_speed": 100,
                "y_speed": 75,
                "max_x_vel": 175,
                "width": 70,
                "height":110,
                "depth": 50,
                "health": 150,
                "max_health": 150,
                "color": (250, 120, 100), #colors are temporary for visual testing
                "attack_range": 80,
                "position_style": "front",
                "reposition_distance": 250,
                "reposition_delay": 1.0,
                "break_threshold": 6,
                "attacks":{
                    "basic punch": {
                        "windup": 0.6,
                        "active": 0.25,
                        "recovery": 0.75,
                        "cooldown": 1.2,
                        "damage": 45,
                        "width": 80,
                        "height": 50,
                        "depth": 55,
                        "lunge": 0,
                        "lunge speed": 0,
                        "charge speed": 0,
                        "weight": 1,
                        "indicator color": (255, 200, 0),
                        "indicator size": 8
                    },
                    "heavy punch": {
                        "windup": 0.9,
                        "active": 0.35,
                        "recovery": 1.0,
                        "cooldown": 1.5,
                        "damage": 60,
                        "width": 100,
                        "height": 65,
                        "depth": 65,
                        "lunge": 65,
                        "lunge speed": 130,
                        "charge speed": 0,
                        "weight": 3,
                        "indicator color": (255, 120, 0),
                        "indicator size": 14
                    }
                }
            },
            "fast":{
                "x_speed": 220,
                "y_speed": 140,
                "max_x_vel": 400,
                "width": 50,
                "height": 65,
                "depth": 45,
                "health": 75,
                "max_health": 75,
                "color": (50, 150, 100), #colors are temporary for visual testing
                "attack_range": 60,
                "position_style": "flank",
                "reposition_distance": 100,
                "reposition_delay": 0.25,
                "break_threshold": 3,
                "attacks":{
                    "basic punch": {
                        "windup": 0.2,
                        "active": 0.125,
                        "recovery": 0.3,
                        "cooldown": 0.4,
                        "damage": 20,
                        "width": 65,
                        "height": 35,
                        "depth": 40,
                        "lunge": 0,
                        "lunge speed": 0,
                        "charge speed": 0,
                        "weight": 4,
                        "indicator color": (255, 200, 0),
                        "indicator size": 8
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
                        "lunge": 85,
                        "lunge speed": 275,
                        "charge speed": 0,
                        "weight": 1,
                        "indicator color": (255, 120, 0),
                        "indicator size": 14
                    }
                }
            }
        }

        self.boss_types = {
            "basic":{
                "x_speed": 100,
                "y_speed": 100,
                "max_x_vel": 300,
                "width": 80,
                "height": 150,
                "depth": 60,
                "health": 300,
                "max_health": 300,
                "color": (150, 250, 100), #colors are temporary for visual testing
                "attack_range": 150,
                "position_style": "front",
                "reposition_distance": 250,
                "reposition_delay": 1.0,
                "break_threshold": 8,
                "attacks":{
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
                        "lunge speed": 0,
                        "weight": 1,
                        "indicator color": (255, 250, 0),
                        "indicator size": 8
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
                        "lunge speed": 180,
                        "weight": 1,
                        "indicator color": (255, 120, 0),
                        "indicator size": 14
                    }
                }
            }
        }

        if not boss:
            self.enemy_data = self.enemy_types[e_type]
        else:
            self.enemy_data = self.boss_types[e_type]

        #movement
        self.x_speed = self.enemy_data["x_speed"]
        self.y_speed = self.enemy_data["y_speed"]
        self.current_slope = None
        self.max_slope_gradient = 0.75
        self.max_x_vel = self.enemy_data["max_x_vel"]
        self.gravity = 980
        self.x_velocity = 0

        #size
        self.width = self.enemy_data["width"]
        self.height = self.enemy_data["height"]
        self.depth = self.enemy_data["depth"]

        #stats
        self.health = self.enemy_data["health"]
        self.max_health = self.enemy_data["max_health"]
        self.alive = True
        self.color = self.enemy_data["color"]

        #combat
        self.been_hit = False
        self.invuln_t = 0.0
        self.invuln_dur = 0.25
        self.attack_range = self.enemy_data["attack_range"]
        self.attacks = self.enemy_data["attacks"]
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
        self.charge_speed = 0
        self.charge_hit_player = False

        #Hit reactions
        self.consecutive_hits = 0
        self.hit_reset_timer = 0.0
        self.hit_reset_delay = 1.0

        #stuns and enemy breaking
        self.hit_stun_timer = 0.0
        self.is_broken = False
        self.flinch_x_velocity = 0

        self.bounce_x_velocity = 0
        self.bounce_z_velocity = 0

        self.break_threshold = self.enemy_data["break_threshold"]
        

        #attack dimensions
        self.atk_w = 0
        self.atk_h = 0
        self.atk_d = 0

        #AI
        self.awareness_range = 400
        self.player_detected = False
        self.state = "idle"
        self.current_attack = "placeholder"
        self.pending_attack = None
        self.attack_phase = ""
        self.attack_timer = 0.0
        self.attack_target_y = 0
        self.target_x = None
        self.target_y = None
        self.has_position = False
        self.position_timer = 0.0
        self.position_style = self.enemy_data["position_style"]
        self.reposition_distance = self.enemy_data["reposition_distance"]
        self.reposition_delay = self.enemy_data["reposition_delay"]
        self.player_was_attacking = False
        self.opening_timer = 0
        self.behavior = behavior
        self.opportunist_commiting = False
        self.wander_chance = 0.02
        self.wander_cooldown = 0
        self.wander_target_x = None
        self.wander_target_y = None
        self.wander_timer = 0


    def get_screen_coords(self, camera_x=0):
        screen_x = self.x - camera_x
        screen_y = self.y - self.z - self.height
    
        return screen_x, screen_y


    def draw(self, screen, camera_x=0):
        scn_x, scn_y = self.get_screen_coords(camera_x)
        pygame.draw.rect(screen, self.color, (scn_x, scn_y, self.width, self.height))
        side = self.attack_range * self.direction
        pygame.draw.line(screen, (250, 50, 0), (self.x + self.width / 2 - camera_x, self.y - self.z - (self.height * 3) /4), (self.x + self.width / 2 + side - camera_x, self.y - self.z - (self.height * 3) /4), 4)

        #attack indicator
        if self.attack_phase == "windup":
            indicator_color = self.enemy_data["attacks"][self.current_attack]["indicator color"]
            indicator_size = self.enemy_data["attacks"][self.current_attack]["indicator size"]     
            pygame.draw.circle(screen, indicator_color, (int(self.x + self.width / 2 - camera_x), int(self.y - self.z - self.height - 15)), indicator_size)
                
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


    def update(self, dt, player, walls, enemies, slopes, cba):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.been_hit = False

        if not self.alive:
            return

        if self.wander_cooldown > 0:
            self.wander_cooldown = max(0, self.wander_cooldown - dt)
        
        if self.player_was_attacking and not player.currently_attacking:
            self.opening_timer = 0.5

            if self.behavior == "opportunist":
                self.opportunist_commiting = True

        self.player_was_attacking = player.currently_attacking

        if self.opening_timer > 0:
            self.opening_timer = max(0, self.opening_timer - dt)

        if self.invuln_t > 0:
            self.invuln_t = max(0, self.invuln_t - dt)

        if self.hit_reset_timer > 0:
            self.hit_reset_timer = max(0, self.hit_reset_timer - dt)

            if self.hit_reset_timer == 0:
                self.consecutive_hits = 0

        if self.attack_cooldown > 0:
            self.attack_cooldown = max(0, self.attack_cooldown - dt)

        self.detect_player(player)
        self.detect_slope(slopes)

        if self.is_broken:
            self.update_break_reaction(dt, walls, player, enemies)
            return

        if self.hit_stun_timer > 0:
            displacement = self.wall_restricted_x(self.flinch_x_velocity * dt, walls, player, enemies, True)

            if displacement == 0:
                self.flinch_x_velocity = 0

            # Gradually slow down the knockback
            self.flinch_x_velocity *= max(0, 1 - 3 * dt)

            self.hit_stun_timer = max(0, self.hit_stun_timer - dt)

            if self.hit_stun_timer == 0:
                self.flinch_x_velocity = 0
                self.position_timer = 0.1

                if self.player_detected:
                    self.state = "chasing"
                else:
                    self.state = "idle"

            return


        self.follow_slope()
        self.slide_on_slope(dt)

        if self.x_velocity != 0:
            displacement = self.wall_restricted_x(self.x_velocity * dt, walls, player, enemies, True)

            if displacement == 0:
                self.x_velocity = 0

        if self.state == "attacking":
            self.update_attack(dt, walls, player, enemies)

        elif self.state == "wandering":
            self.update_wandering(dt, walls, player, enemies, cba)

        else:
            self.combat_checks(player, dt, walls, enemies, cba)

        if self.flinch_x_velocity != 0:
            displacement = self.wall_restricted_x(self.flinch_x_velocity * dt, walls, player, enemies, True)

            if displacement == 0:
                self.flinch_x_velocity = 0

            self.flinch_x_velocity *= max(0, 1 - 5 * dt)
            


    def combat_checks(self, player, dt, walls, enemies, cba):
        player_center = player.x + player.width / 2
        enemy_center = self.x + self.width / 2

        if player_center > enemy_center:
            self.direction = 1
        else:
            self.direction = -1

        if self.player_detected:
            if self.wander_cooldown <= 0:
                if random.random() < self.wander_chance * dt:
                    self.start_wandering(cba)
                    return

            if self.opportunist_commiting:
                self.has_position = False
                self.state = "chasing"

                if not self.in_attack_range(player):
                    self.pursue(player, dt, walls, enemies)
                    return

            else:
                if self.has_position:
                    self.position_timer += dt

                    dx = abs(player.x - self.target_x)
                    dy = abs(player.y - self.target_y)

                    if (dx > self.reposition_distance or dy > self.reposition_distance) and self.position_timer >= self.reposition_delay:
                        self.has_position = False

                if not self.has_position:
                    self.choose_position(player, enemies, walls)

                    if self.has_position:
                        self.state = "repositioning"

            if self.state == "repositioning":
                self.move_to_position(dt, walls, player, enemies)

                dx = abs(self.target_x - self.x)
                dy = abs(self.target_y - self.y)

                if dx <= 5 and dy <= 5:
                    self.state = "chasing"

            elif self.in_attack_range(player) and self.attack_cooldown <= 0 and self.can_attack(enemies):
                if self.state != "attacking":
                    self.state = "attacking"

                    if self.behavior == "opportunist":
                        self.opportunist_commiting = False
                    
                    self.attack_phase = "windup"
                    self.attack_timer = 0
                    self.attack_target_y = player.y - player.depth / 2

                    if self.pending_attack is None:
                        #choose an attack
                        attacks = list(self.attacks.keys())
                        weights = []

                        for attack in attacks:
                            weights.append(self.attacks[attack]["weight"])

                        self.pending_attack = random.choices(attacks, weights=weights)[0]

                    self.current_attack = self.pending_attack

                    if self.current_attack == "charge":
                        enemy_y = self.y - self.depth / 2
                        player_y = player.y - player.depth / 2

                        if abs(enemy_y - player_y) > 15:
                            self.target_y = player_y + self.depth / 2
                            self.target_x = self.x
                            self.has_position = True
                            self.state = "repositioning"
                            return

                    atk_data = self.attacks[self.current_attack]
        
                    #assign data
                    self.attack_damage = atk_data["damage"]
                    self.lunge = atk_data["lunge"]
                    self.lunge_speed = atk_data["lunge speed"]
                    self.lunge_dist = 0
                    self.windup_duration = atk_data["windup"]
                    self.active_duration = atk_data["active"]
                    self.recovery_duration = atk_data["recovery"]
                    self.charge_speed = atk_data.get("charge speed", 0)
                    self.charge_hit_player = False
        
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


    def detect_slope(self, slopes):
        self.current_slope = None

        for slope in slopes:
            if slope.overlaps_player(self):
                self.current_slope = slope
                break


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

        
        move_x = 0

        if dx > self.attack_range:
            move_x = min(dx - self.attack_range, self.x_speed * dt)

            if p_cntr_x < e_cntr_x:
                move_x *= -1

            if self.current_slope is not None:
                if self.current_slope.gradient >= self.max_slope_gradient:
                    if move_x * self.current_slope.direction > 0:
                        move_x = 0

        displacement = self.wall_restricted_x(move_x, walls, player, enemies)

        if displacement == 0 and move_x != 0:
            self.x_velocity = 0

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
            if self.current_attack == "charge" and not self.charge_hit_player:
                movement = self.charge_speed * dt * self.attack_direction

                # Check whether the next movement would hit the player
                self.x += movement
                hit_player = self.check_body_collision(player)
                self.x -= movement

                if hit_player:
                    if player.invuln_t <= 0:
                        player.take_damage(self.attack_damage)

                    self.charge_hit_player = True
                    self.attack_timer = self.active_duration

                else:
                    displacement = self.wall_restricted_x(movement, walls, player, enemies)

                    if displacement == 0:
                        self.attack_timer = self.active_duration

            if self.attack_timer >= self.active_duration:
                self.attack_phase = "recovery"
                self.attack_timer = 0

        elif self.attack_phase == "recovery":
            if self.attack_timer >= self.recovery_duration:
                self.attack_phase = ""
                self.attack_timer = 0
                self.attack_cooldown = self.attack_cooldown_duration
                self.current_attack = "placeholder"
                self.pending_attack = None
                
                if self.has_position:
                    self.state = "repositioning"
                else:
                    self.state = "chasing"


    def get_attack_hitbox(self):
        if self.current_attack == "charge":
            return None
        
        if self.attack_phase == "active":

            atk_y = self.attack_target_y + (self.atk_d/2)
    
            if self.attack_direction == -1:
                punch_x = self.x - self.atk_w
            elif self.attack_direction == 1:
                punch_x = self.x + self.width
    
            hitbox = (punch_x, atk_y, self.z, self.atk_w, self.atk_h, self.atk_d)
    
            return hitbox
            
        else:
            return None


    #Temporary hitbox debugging tool
    def draw_attack_hitbox(self, screen, camera_x=0):
        hitbox = self.get_attack_hitbox()

        if hitbox is not None:
            x, y, z, w, h, d = hitbox

            # Convert world coordinates to screen coordinates
            screen_x = x - camera_x
            screen_y = y - z - h

            # Draw a transparent red rectangle
            debug_surface = pygame.Surface((w, h), pygame.SRCALPHA)
            debug_surface.fill((255, 0, 0, 100))

            screen.blit(debug_surface, (screen_x, screen_y))

            # Draw the outline
            pygame.draw.rect(screen, (255, 0, 0), (screen_x, screen_y, w, h), 2)


    def wall_restricted_x(self, movement, walls, player, enemies, ignore_player=False):
        previous_x = self.x
        self.x += movement

        for wall in walls:
            if wall.check_col(self):
                self.x = previous_x
                break

        if not ignore_player and self.check_body_collision(player):
            self.x = previous_x

        for enemy in enemies:
            if enemy is not self and enemy.alive and self.check_enemy_collision(enemy):
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
            if enemy is not self and enemy.alive and self.check_enemy_collision(enemy):
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


    def check_enemy_collision(self, other):
        mini_w = self.width * 0.5
        mini_d = self.depth * 0.5

        mini_w_other = other.width * 0.5
        mini_d_other = other.depth * 0.5

        mini_x = self.x + (self.width - mini_w) / 2
        mini_x_other = other.x + (other.width - mini_w_other) / 2

        mini_y = self.y - (self.depth - mini_d) / 2
        mini_y_other = other.y - (other.depth - mini_d_other) / 2

        # X overlap
        if mini_x + mini_w <= mini_x_other or mini_x >= mini_x_other + mini_w_other:
            return False
        
        # Y overlap
        if mini_y <= mini_y_other - mini_d_other or mini_y - mini_d >= mini_y_other:
            return False
        
        # Z overlap
        if self.z + self.height <= other.z or self.z >= other.z + other.height:
            return False
        
        return True


    def follow_slope(self):
        if self.current_slope is not None:
            self.z = self.current_slope.get_player_surface_height(self)

        else:
            self.z = 0


    def slide_on_slope(self, dt):
        if self.current_slope is None:
            self.x_velocity = 0
            return

        if self.current_slope.gradient < self.max_slope_gradient:
            self.x_velocity = 0
            return

        slope_angle = math.atan(self.current_slope.gradient)
        acceleration = self.gravity * math.sin(slope_angle)

        if self.current_slope.direction == 1:
            acceleration *= -1

        self.x_velocity += acceleration * dt
        self.x_velocity = max(-self.max_x_vel, min(self.max_x_vel, self.x_velocity))


    def choose_position(self, player, enemies, walls):
        self.has_position = False
        if self.position_style == "balanced":
            positions = [(-150, 0), (150, 0), (-120, -70), (120, -70), (-120, 70), (120, 70)]

        elif self.position_style == "front":
            positions = [(-150, 0), (150, 0), (-120, 70), (120, 70), (-120, -70), (120, -70)]

        elif self.position_style == "flank":
            positions = [(-70, -70), (70, -70), (-70, 70), (70, 70), (-100, 0), (100, 0)]

        best_position = None
        best_distance = float("inf")

        for offset_x, offset_y in positions:
            target_x = player.x + offset_x
            target_y = player.y + offset_y

            blocked = False

            for wall in walls:
                if (target_x < wall.x + wall.width and target_x + self.width > wall.x and target_y > wall.y - wall.depth and target_y - self.depth < wall.y and self.z < wall.z + wall.height and self.z + self.height > wall.z):
                    blocked = True
                    break

                if blocked:
                    continue

                if (target_x < player.x + player.width and target_x + self.width > player.x and target_y > player.y - player.depth and target_y - self.depth < player.y and self.z < player.z + player.z + player.height and self.z + self.height > player.z):
                    continue

            occupied = False

            for enemy in enemies:
                if enemy is not self and enemy.has_position:
                    dx = abs(enemy.target_x - target_x)
                    dy = abs(enemy.target_y - target_y)

                    if dx < 50 and dy < 40:
                        occupied = True
                        break

            if not occupied:
                dx = target_x - self.x
                dy = target_y - self.y

                distance = math.sqrt(dx ** 2 + dy ** 2)

                if distance < best_distance:
                    best_distance = distance
                    best_position = (target_x, target_y)

        if best_position is not None:
            self.target_x, self.target_y = best_position
            self.has_position = True
            self.position_timer = 0.0


    def move_to_position(self, dt, walls, player, enemies):
        dx = self.target_x - self.x

        if abs(dx) > 5:
            move_x = min(abs(dx), self.x_speed * dt)

            if dx < 0:
                move_x *= -1

            self.wall_restricted_x(move_x, walls, player, enemies)

        dy = self.target_y - self.y

        if abs(dy) > 5:
            move_y = min(abs(dy), self.y_speed * dt)

            if dy < 0:
                move_y *= -1

            self.wall_restricted_y(move_y, walls, player, enemies)


    def draw_position_target(self, screen, camera_x=0):
        if self.has_position:
            screen_x = self.target_x - camera_x
            screen_y = self.target_y - self.z - 10

            pygame.draw.circle(
                screen,
                (255, 255, 0),
                (int(screen_x), int(screen_y)),
                8,
                2
            )

            pygame.draw.line(screen, (255, 255, 0), (int(self.x + self.width / 2 - camera_x), int(self.y - self.z - self.height / 2)),(int(screen_x), int(screen_y)), 1)


    def can_attack(self, enemies):
        attackers = 0

        for enemy in enemies:
            if enemy is not self and enemy.alive:
                if enemy.state == "attacking":
                    attackers += 1

        if attackers >= 3:
            return False

        return True


    def receive_hit(self, attack_direction):
        if self.is_broken:
            return

        self.consecutive_hits += 1
        self.hit_reset_timer = self.hit_reset_delay

        self.attack_phase = ""
        self.attack_timer = 0

        if self.consecutive_hits >= self.break_threshold:
            self.is_broken = True
            self.state = "broken"

            self.bounce_x_velocity = attack_direction * 350
            self.bounce_z_velocity = 400

        else:
            self.state = "flinching"
            self.hit_stun_timer = 0.15
            self.flinch_x_velocity = attack_direction * 100


    def update_break_reaction(self, dt, walls, player, enemies):

        displacement = self.wall_restricted_x(self.bounce_x_velocity * dt, walls, player, enemies)

        if displacement == 0:
            self.bounce_x_velocity = 0

        self.bounce_x_velocity *= max(0, 1 -3 * dt)

        self.z += self.bounce_z_velocity * dt
        self.bounce_z_velocity -= self.gravity * dt

        ground_z = 0

        if self.current_slope is not None:
            ground_z = self.current_slope.get_player_surface_height(self)

        if self.z <= ground_z:
            self.z = ground_z

            self.bounce_x_velocity = 0
            self.bounce_z_velocity = 0

            self.is_broken = False
            self.consecutive_hits = 0

            if self.player_detected:
                self.state = "chasing"
            else:
                self.state = "idle"


    def start_wandering(self, combat_area):
        self.state = "wandering"
        self.has_position = False

        # Choose a random destination inside the combat area
        self.wander_target_x = random.uniform(combat_area.left, combat_area.right - self.width)

        self.wander_target_y = random.uniform(combat_area.top + self.depth, combat_area.bottom)

        self.wander_timer = 6.0
        self.wander_cooldown = 5.0


    def update_wandering(self, dt, walls, player, enemies, combat_area):
        self.wander_timer -= dt

        dx = self.wander_target_x - self.x
        dy = self.wander_target_y - self.y

        if abs(dx) <= 5 and abs(dy) <= 5:
            self.wander_target_x = None
            self.wander_target_y = None
            self.has_position = None
            self.position_timer = 0
            self.state = "chasing"
            return

        if self.wander_timer <= 0 or not self.player_detected:
            self.wander_target_x = None
            self.wander_target_y = None
            self.has_position = False
            self.position_timer = 0

            if self.player_detected:
                self.state = "chasing"
            else:
                self.state = "idle"
            return

        # Face the direction of horizontal movement
        if dx > 0:
            self.direction = 1
        elif dx < 0:
            self.direction = -1

        self.target_x = self.wander_target_x
        self.target_y = self.wander_target_y

        # Move toward the destination
        self.move_to_position(dt, walls, player, enemies)
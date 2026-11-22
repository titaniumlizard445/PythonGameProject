#Stores player information and interactions in Specific Class
import pygame
import math

class Player:

    def __init__(self):
        #POSITION
        #left and right
        self.x = 100
        
        #depth
        self.y = 100

        #height
        self.z = 0

        self.direction = 1

        #velocities
        self.x_velocity = 0
        self.y_velocity = 0
        self.z_velocity = 0
        self.max_x_vel = 300
        self.max_y_vel = 200

        #accelerations
        self.gravity = 980
        self.x_accel = 1200
        self.x_deccel = 1800
        self.y_accel = 1200
        self.y_deccel = 1800

        #dimensions
        self.width = 40
        self.height = 60
        self.depth = 40

        #Jumping
        self.jump_strength = 400
        self.jumps_remaining = 1
        self.is_grounded = True
        self.total_jumps = 2
        self.coyote_dur = 0.2
        self.coyote_t = 0.0
        self.jump_buf_dur = 0.12
        self.jump_buf_t = 0.0

        #Attacking
        self.jab_w = 50
        self.jab_h = 30
        self.jab_d = 45
        self.currently_attacking = False
        self.attack_cooldown = 0.0
        self.attack_duration = 0.2
        self.attack_direction = None
        self.invuln_t = 0.0
        self.invuln_dur = 0.4

        #Environment detection
        self.current_platform = None
        self.current_slope = None
        self.max_slope_gradient = 0.75

        #Player stats
        self.health = 100
        self.max_health = 100
        self.alive = True
        self.mana = 50

        #player display [Temporary colored box]
        self.color = (20, 50 , 150)


    #METHODS FOR MOVEMENT AND VELOCITY #####################################################


    def move_x(self, dt):
        self.x += self.x_velocity*dt


    def move_y(self, dt):
        self.y += self.y_velocity*dt


    def move_z(self, dt):
        self.z += self.z_velocity*dt


    def wall_restricted_movements(self, delta_time, walls):

        #attempt X
        previous_x = self.x
        self.move_x(delta_time)

        for wall in walls:
            if wall.check_col(self):
                self.x = previous_x
                self.x_velocity = 0
                break

        #attempt Y
        previous_y = self.y
        self.move_y(delta_time)

        for wall in walls:
            if wall.check_col(self):
                self.y = previous_y
                self.y_velocity = 0
                break

    
    def deccelerate(self, delta_time, vel, deccel):
        if abs(vel) > 0:
            #prevents wiggling
            if abs(vel) < 50 and abs(vel) > 0:
                vel = 0

            #actual decceleration control
            elif vel > 0:
                vel = max(0, vel - deccel*delta_time)
            elif vel < 0:
                vel = min(0, vel + deccel*delta_time)

        return vel


    def slide_on_slope(self, dt):
        slope = self.current_slope

        if slope is None:
            return


        if slope.gradient > self.max_slope_gradient:
            slope_angle = math.atan(slope.gradient)

            slide_accel = self.gravity * math.sin(slope_angle)

            downhill_direction = -slope.direction

            self.x_velocity += downhill_direction * slide_accel * dt

            self.x_velocity = max(-self.max_x_vel, min(self.max_x_vel, self.x_velocity))
            


    def kinematic_x(self, delta_time, norm_x):
        self.x_velocity = self.x_velocity + self.x_accel*norm_x*delta_time
        
        if abs(self.x_velocity) > self.max_x_vel:
            if self.x_velocity > 0:
                self.x_velocity = self.max_x_vel
            elif self.x_velocity < 0:
                self.x_velocity = (-1)*self.max_x_vel

        on_steep_slope = False
        if self.current_slope is not None and self.current_slope.gradient > self.max_slope_gradient:
            on_steep_slope = True
        
        if norm_x == 0 and not on_steep_slope:
            self.x_velocity = self.deccelerate(delta_time, self.x_velocity, self.x_deccel)


    def kinematic_y(self, delta_time, norm_y):
        
        self.y_velocity = self.y_velocity + self.y_accel*norm_y*delta_time

        if abs(self.y_velocity) > self.max_y_vel:
            if self.y_velocity > 0:
                self.y_velocity = self.max_y_vel
            elif self.y_velocity < 0:
                self.y_velocity = (-1)*self.max_y_vel

        if norm_y == 0:
            self.y_velocity = self.deccelerate(delta_time, self.y_velocity, self.y_deccel)

    
    def velocity_normalization(self, keyboard_inputs):
        #Velocity Normalization
        input_x = 0
        input_y = 0
        norm_x = 0
        norm_y = 0

        if not (keyboard_inputs[pygame.K_w] and keyboard_inputs[pygame.K_s]):
            if keyboard_inputs[pygame.K_w]:
                input_y = -1
            if keyboard_inputs[pygame.K_s]:
                input_y = 1
        
        if not (keyboard_inputs[pygame.K_d] and keyboard_inputs[pygame.K_a]):
            if keyboard_inputs[pygame.K_a]:
                input_x = -1
                self.direction = -1
            if keyboard_inputs[pygame.K_d]:
                input_x = 1
                self.direction = 1

        magnitude = math.sqrt((input_x**2)+(input_y**2))

        if magnitude != 0:
            norm_x = input_x/magnitude
            norm_y = input_y/magnitude

        return norm_x, norm_y
    
    
    def kinematic_updates(self, keyboard_inputs, delta_time, platforms, walls, slopes):
        
        #movement
        norm_x, norm_y = self.velocity_normalization(keyboard_inputs)

        if (self.current_slope is not None and self.current_slope.gradient > self.max_slope_gradient):
            downhill_direction = -self.current_slope.direction

            if norm_x * downhill_direction < 0:
                norm_x = 0


        self.kinematic_x(delta_time,norm_x)
        self.kinematic_y(delta_time,norm_y)
        #jumping
        self.apply_gravity(delta_time)

        previous_z = self.z
        previous_x = self.x
        previous_y = self.y

        #move
        self.wall_restricted_movements(delta_time, walls)
        self.move_z(delta_time)

        self.detect_pl_collision(platforms, previous_x, previous_y, previous_z)
        self.detect_ground()
        self.detect_slope_col(slopes, previous_z)
        self.slide_on_slope(delta_time)
        self.update_coyote_time(delta_time)
        self.update_jump_buffer(delta_time)


    #METHODS FOR JUMPING AND GRAVITY ##########################################################


    def jump(self):
        if self.jumps_remaining > 0:
            self.z_velocity = self.jump_strength
            self.is_grounded = False
            self.jumps_remaining -= 1
            self.current_slope = None

    
    def request_jump(self):
        if self.jumps_remaining > 0:
            self.jump()
        else:
            self.jump_buf_t = self.jump_buf_dur

    
    def update_jump_buffer(self, delta_time):
        if self.jump_buf_t <= 0:
            return

        if self.jumps_remaining > 0:
            self.jump()
            self.jump_buf_t = 0

        else:
            self.jump_buf_t = max(0, self.jump_buf_t - delta_time)


    def update_coyote_time(self, delta_time):

        if self.is_grounded:
            self.coyote_t = self.coyote_dur

        elif self.coyote_t > 0:
            self.coyote_t = max(0, self.coyote_t - delta_time)

            if self.coyote_t == 0:
                if self.jumps_remaining == self.total_jumps:
                    self.jumps_remaining -= 1
            

    def apply_gravity(self, delta_time):
        if not self.is_grounded:
            self.z_velocity -= self.gravity * delta_time


    def update_ground(self):
        self.z_velocity = 0
        self.is_grounded = True
        self.jumps_remaining = self.total_jumps


    def detect_ground(self):
        if self.z <= 0:
            self.z = 0
            self.update_ground()



    #METHODS FOR COMBAT ##################################################################


    def attack(self):
        if self.attack_cooldown <= 0 and not self.currently_attacking:
            self.currently_attacking = True
            self.attack_cooldown = self.attack_duration
            self.attack_direction = self.direction


    def update_attack(self, dt):
        if self.currently_attacking:
            self.attack_cooldown -= dt
            if self.attack_cooldown <= 0:
                self.attack_cooldown = 0
                self.currently_attacking = False

    
    def get_attack_hitbox(self):
        if self.currently_attacking:
            self.atk_y = (self.y - (self.depth / 2)) + (self.jab_d/2)

            if self.attack_direction == -1:
                if self.x_velocity != 0 and self.is_grounded:
                    jab_x = self.x - self.jab_w
                else:
                    jab_x = self.x - self.jab_h
            elif self.attack_direction == 1:
                jab_x = self.x + self.width
            else:
                jab_x = None

            #if attack is horizontal
            if self.is_grounded:

                #forward jab
                if self.x_velocity != 0:
                    hitbox = (jab_x, self.atk_y, self.z, self.jab_w, self.jab_h, self.jab_d)
                
                #stationary upward jab
                else:
                    hitbox = (jab_x, self.atk_y , self.z, self.jab_h, self.jab_w, self.jab_d)
            
            #basic aerial jab
            else:
                hitbox = (jab_x, self.atk_y, self.z, self.jab_h, self.jab_w, self.jab_d)

            #hitbox = tuple (xpos, ypos, jab width, jab height, jab depth)
            return hitbox
        
        else:
            return None


    def draw_attack(self, screen, hitbox):
        drawable_hit = list(hitbox)
        drawable_hit.remove(self.jab_d)
        drawable_hit.remove(self.atk_y)

        x, z, w, h = drawable_hit

        if not self.is_grounded:
            new_hitbox = (x, 0 - z + self.y, w, h)
        elif self.x_velocity != 0:
            new_hitbox = (x, self.y - z - self.height, w, h)
        else:
            new_hitbox = (x, self.y - z - (1.75 * self.height), w, h)

        pygame.draw.rect(screen, (120, 120, 0), new_hitbox, 2)


    def check_col(self, incoming_hitbox):
        atk_x, atk_y, atk_z, atk_w, atk_h, atk_d = incoming_hitbox
        if self.x + self.width >= atk_x  and self.x  <= atk_x + atk_w:
            if self.y >= atk_y - atk_d and self.y - self.depth <= atk_y:
                if self.z + self.height >= atk_z  and self.z  <= atk_z + atk_h:
                    return True

        return False


    def update_invuln(self, dt):
        self.invuln_t = max(0, self.invuln_t - dt)


    #METHODS FOR PLATFORM COLLISION ######################################################

    
    def over_platform(self, platform):
        if self.x + self.width > platform.x and self.x < platform.x + platform.width:
            if self.y > platform.y - platform.depth and self.y - self.depth < platform.y:
                return True
            
            else:
                return False
        else:
            return False


    def over_plat_location(self, platform, x, y):

        if x + self.width > platform.x and x < platform.x + platform.width:
            if y > platform.y - platform.depth and y - self.depth < platform.y:
                return True

        return False


    def detect_pl_collision(self, platforms, previous_x, previous_y, previous_z):

        landing_platform = None

        for platform in platforms:


            # Landing on the platform - checks if a player is passing through a platform
            if (previous_z > platform.z and self.z <= platform.z and self.z_velocity < 0):

                #Find when the player crosses the platform
                t = (previous_z - platform.z) / (previous_z - self.z)

                #find X and Y position at the moment of landing
                land_x = previous_x + (self.x - previous_x) * t
                land_y = previous_y + (self.y - previous_y) * t

                #detect footprint overlap at moment of landing
                if self.over_plat_location(platform, land_x, land_y):
                    
                    if landing_platform is None or platform.z > landing_platform.z:
                        landing_platform = platform   

            # Already standing on the platform
            elif abs(self.z - platform.z) < 0.001 and self.z_velocity == 0 and self.over_platform(platform):
                if landing_platform is None or platform.z > landing_platform.z:
                    landing_platform = platform

        #player is standing on a platform
        if landing_platform is not None:
            self.update_ground()
            self.z = landing_platform.z
            self.current_platform = landing_platform

        else:
            self.current_platform = None

            if self.z > 0:
                if self.current_slope is None:
                    self.is_grounded = False
            else:
                self.z = 0
                self.update_ground()


    #METHODS FOR SLOPE COLLSION #################################################################

    def detect_slope_col(self, slopes, previous_z):
        found_slope = False
        for slope in slopes:
            if slope.overlaps_player(self):
                height = slope.get_player_surface_height(self)
                found_slope = True
                #just stepped foot on the slope
                if previous_z > height and self.z <= height and self.z_velocity < 0:
                    self.update_ground()
                    self.z = height + 1
                    self.current_slope = slope

                #currently on or above the slope
                elif self.is_grounded and (self.current_slope == slope or self.current_slope is None):
                    self.z = height + 1
                    self.current_slope = slope

        if found_slope == False:
            self.current_slope = None


    #GAME UPDATE METHOD ####################################################################

    
    def update(self, keyboard_inputs, delta_time, platforms, walls, slopes):
        #useful for adding movement and animations
        if self.health == 0:
            self.alive = False

        self.kinematic_updates(keyboard_inputs, delta_time, platforms, walls, slopes)
        self.update_attack(delta_time)
        self.update_invuln(delta_time)


    # METHODS FOR DEPTH SORTING AND PROPERTIES ###############################################

    
    @property
    def full_speed(self):
        return math.sqrt(
            self.x_velocity**2 +
            self.z_velocity**2 +
            self.y_velocity**2
        )


    @property
    def depth_sort(self):
        return self.y - self.depth / 2


    @property
    def sort_z(self):
        return self.z + self.height / 2


    @property
    def sort_value(self):
        return self.depth_sort + (self.sort_z * 0.5)


    #METHODS FOR RENDERING ###################################################################

    
    def get_screen_coords(self):
        screen_x = self.x 
        screen_y = self.y - self.z - self.height

        return screen_x, screen_y


    def get_shadow_height(self, platforms, slopes):
        shadow_z = 0

        for platform in platforms:
            if platform.z <= self.z and self.over_platform(platform):
                if platform.z > shadow_z:
                    shadow_z = platform.z

        for slope in slopes:
            if slope.overlaps_player(self):
                s_height = slope.get_player_surface_height(self)
                if self.z >= s_height and s_height > shadow_z:
                    shadow_z = s_height

        return shadow_z


    def draw(self, screen):
        scn_x, scn_y = self.get_screen_coords()
        pygame.draw.rect(screen, self.color, (scn_x, scn_y, self.width, self.height))


    def get_vis_bounds(self):
        return (self.x, self.x + self.width, self.y - self.z - self.height, self.y - self.z)


    def get_shadow_bounds(self, platforms, slopes):
        shad_z = self.get_shadow_height(platforms, slopes)
        return (self.x, self.x + self.width, self.y - shad_z, self.y - shad_z + 10)


    def draw_shadow(self, screen, platforms, slopes):
        shad_z = self.get_shadow_height(platforms, slopes)
        pygame.draw.ellipse(screen, (40, 40, 40), (self.x, self.y - shad_z, self.width, 10), 0)


    #METHODS FOR PLAYER STATS ###############################################################

    def take_damage(self, incoming_damage):
        if self.invuln_t <= 0:
            self.health = max(0, (self.health - incoming_damage))
            self.invuln_t = self.invuln_dur


    def heal(self, amount):
        if self.health == 0:
            pass
        else:
            self.health += amount
            if self.health > self.max_health:
                self.health = self.max_health

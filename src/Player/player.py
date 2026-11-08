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

        #Player stats
        self.health = 100
        self.max_health = 100
        self.alive = True
        self.mana = 50

        #player display [Temporary colored box]
        self.color = (20, 50 , 150)


    def move_x(self, dt):
        self.x += self.x_velocity*dt


    def move_y(self, dt):
        self.y += self.y_velocity*dt


    def move_z(self, dt):
        self.z += self.z_velocity*dt


    def jump(self):
        if self.jumps_remaining > 0:
            self.z_velocity = self.jump_strength
            self.is_grounded = False
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


    def kinematic_x(self, delta_time, norm_x):
        self.x_velocity = self.x_velocity + self.x_accel*norm_x*delta_time
        
        if abs(self.x_velocity) > self.max_x_vel:
            if self.x_velocity > 0:
                self.x_velocity = self.max_x_vel
            elif self.x_velocity < 0:
                self.x_velocity = (-1)*self.max_x_vel
        
        if norm_x == 0:
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
            if keyboard_inputs[pygame.K_d]:
                input_x = 1

        magnitude = math.sqrt((input_x**2)+(input_y**2))

        if magnitude != 0:
            norm_x = input_x/magnitude
            norm_y = input_y/magnitude

        return norm_x, norm_y


    def over_platform(self, platform):
        if self.x + self.width > platform.x and self.x < platform.x + platform.width:
            if self.y + self.depth > platform.y and self.y < platform.y + platform.depth:
                return True
            
            else:
                return False
        else:
            return False

    def detect_pl_collision(self, platform, previous_z):

        if self.over_platform(platform):

            # Landing on the platform
            if (previous_z >= platform.z and
                self.z <= platform.z and
                self.z_velocity < 0):

                self.z = platform.z
                self.update_ground()

            # Already standing on the platform
            elif self.z == platform.z and self.z_velocity == 0:
                self.update_ground()

        else:
            self.is_grounded = False
    

    def kinematic_updates(self, keyboard_inputs, delta_time, platform,):
        
        #movement
        norm_x, norm_y = self.velocity_normalization(keyboard_inputs)
        self.kinematic_x(delta_time,norm_x)
        self.kinematic_y(delta_time,norm_y)
        #jumping
        self.apply_gravity(delta_time)

        previous_z = self.z
        #move
        self.move_x(delta_time)
        self.move_y(delta_time)
        self.move_z(delta_time)

        self.detect_ground()
        self.detect_pl_collision(platform, previous_z)


    def update(self, keyboard_inputs, delta_time, platform):
        #useful for adding movement and animations
        if self.health == 0:
            self.alive = False

        self.kinematic_updates(keyboard_inputs, delta_time, platform)
        
        
    @property
    def full_speed(self):
        return math.sqrt(
            self.x_velocity**2 +
            self.z_velocity**2 +
            self.y_velocity**2
        )


    def draw(self, screen):
        pygame.draw.rect(
            screen,
            self.color,
            (self.x, self.y - self.z - self.height, self.width, self.height)
        )


    def take_damage(self, incoming_damage):
        self.health = max(0, (self.health - incoming_damage))


    def heal(self, amount):
        if self.health == 0:
            pass
        else:
            self.health += amount
            if self.health > self.max_health:
                self.health = self.max_health

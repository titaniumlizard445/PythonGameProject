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
        self.max_z_vel = 0 #placeholder

        #accelerations
        self.gravity = 980
        self.x_accel = 1200
        self.x_deccel = 1800

        #dimensions
        self.width = 40
        self.height = 60

        #Jumping
        self.jump_strength = 12

        #Player stats
        self.health = 100
        self.max_health = 100
        self.alive = True
        self.mana = 50

        #player display [Temporary colored box]
        self.color = (20, 50 , 150)

    def move_x(self, dt):
        self.x += self.x_velocity*dt

    def deccelerate(self, delta_time):
        if abs(self.x_velocity) > 0:
            #prevents wiggling
            if abs(self.x_velocity) < 50 and abs(self.x_velocity) > 0:
                self.x_velocity = 0

            #actual decceleration control
            elif self.x_velocity > 0:
                self.x_velocity = self.x_velocity - self.x_deccel*delta_time
            elif self.x_velocity < 0:
                self.x_velocity = self.x_velocity + self.x_deccel*delta_time

    def kinematic_updates(self, keyboard_inputs, delta_time):
        #movement
                
        #if both:
        if keyboard_inputs[pygame.K_a] and keyboard_inputs[pygame.K_d]:
            self.deccelerate(delta_time)
                
        #accelerate left
        elif keyboard_inputs[pygame.K_a]:
            if self.x_velocity > (-1)*self.max_x_vel:
                self.x_velocity = self.x_velocity + ((-1)*self.x_accel)*delta_time
            elif self.x_velocity < (-1)*self.max_x_vel:
                self.x_velocity = (-1)*self.max_x_vel
        
        #accelerate right
        elif keyboard_inputs[pygame.K_d]:
            if self.x_velocity < self.max_x_vel:
                self.x_velocity = self.x_velocity + self.x_accel*delta_time
            elif self.x_velocity > self.max_x_vel:
                self.x_velocity = self.max_x_vel
        
        else:
            self.deccelerate(delta_time)

        #move
        self.move_x(delta_time)

    def update(self, keyboard_inputs, delta_time):
        #useful for adding movement and animations
        if self.health == 0:
            self.alive = False

        self.kinematic_updates(keyboard_inputs, delta_time)

        
        
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
            (self.x, self.y, self.width, self.height)
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

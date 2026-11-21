import pygame
import settings
from src.Player.player import Player
from src.Environment.platform import Platform
from src.Environment.wall import Wall
from src.Environment.renderer import Renderer
from src.Enemies.enemy import Enemy

pygame.init()

#window
screen = pygame.display.set_mode(
    (settings.screen_width, settings.screen_height)
)

pygame.display.set_caption(settings.window_title)

#frames
clock = pygame.time.Clock()

running = True

#Object Creation

r = Renderer()

player = Player()

platform = Platform(200, 470, 20, 400, 30, 40)
platforms = [platform]

wall = Wall(200, 500, 20, 400, 30, 40)
walls = [wall]

enemy = Enemy(400, 300)
enemies = [enemy]

while running:

    #event handler
    for event in pygame.event.get():

        #player closes window 
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.request_jump()

            elif event.key == pygame.K_j:
                player.attack()

    #Fps step
    dt = clock.tick(settings.fps) / 1000

    #background
    screen.fill(settings.bg_color)

    #Character Controls
    keys = pygame.key.get_pressed()
    player.update(keys, dt, platforms, walls)

    #enemy updates
    for enemy in enemies:
        enemy.update(dt)

    enemies = [enemy for enemy in enemies if enemy.alive]

    # Build environment


    r.draw_scene(screen, player, platforms, walls, enemies)


    if player.currently_attacking:
        atk_hitbox = player.get_attack_hitbox()

        player.draw_attack(screen, atk_hitbox)

        for enemy in enemies:
            if enemy.invuln_t <= 0 and enemy.check_col(atk_hitbox):
                enemy.been_hit = True
                enemy.health -= 25
                enemy.invuln_t = enemy.invuln_dur

    #display update
    pygame.display.flip()


pygame.quit()
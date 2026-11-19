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
wall = Wall(800, 250, 0, 50, 50, 50)

wall_top = Platform(wall.x, wall.y, wall.z + wall.height, wall.width, 20, wall.depth)

test_player = Player()
test_platform3 = Platform(800, 400, 20, 200, 20, 100)
platforms = [test_platform3, wall_top]

test_wall1 = Wall(300, 200, 0, 50, 50, 50)
test_wall2 = Wall(400, 400, 0, 50, 100, 50)
test_wall3 = Wall(700, 500, 0, 100, 60, 20)
test_wall4 = Wall(700, 400, 0, 100, 60, 20)
test_wall5 = Wall(750, 375, 20, 50, 50, 50)
walls = [test_wall1, test_wall2, test_wall3, test_wall4, wall, test_wall5]

test_enemy1 = Enemy(200,200)
enemies = [test_enemy1]
while running:

    #event handler
    for event in pygame.event.get():

        #player closes window 
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                test_player.request_jump()

            elif event.key == pygame.K_j:
                test_player.attack()

    #Fps step
    dt = clock.tick(settings.fps) / 1000

    #background
    screen.fill(settings.bg_color)

    #Character Controls
    keys = pygame.key.get_pressed()
    test_player.update(keys, dt, platforms, walls)

    #enemy updates
    e_copy = enemies.copy()
    for e in enemies:
        e.update(dt)
        if not e.alive:
            e_copy.remove(e)

    enemies = e_copy

    #print("Platform:", test_player.current_platform, "Grounded:", test_player.is_grounded)

    # Build environment

    r = Renderer()

    r.draw_scene(screen, test_player, platforms, walls, enemies)

    if test_player.currently_attacking:
        atk_hitbox = test_player.get_attack_hitbox()

        test_player.draw_attack(screen, atk_hitbox)

        for enemy in enemies:
            if enemy.invuln_t <= 0 and enemy.check_col(atk_hitbox):
                enemy.been_hit = True
                enemy.health -= 25
                enemy.invuln_t = enemy.invuln_dur



    
    #display update
    pygame.display.flip()



pygame.quit()
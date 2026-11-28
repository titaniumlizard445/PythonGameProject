import pygame
import settings
from src.Player.player import Player
from src.Environment.platform import Platform
from src.Environment.wall import Wall
from src.Environment.renderer import Renderer
from src.Enemies.enemy import Enemy
from src.Environment.slope import Slope
from src.Environment.combat_area import CombatArea
from src.Environment.camera import Camera

pygame.init()

death_font = pygame.font.Font(None, 90)

#window
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))

pygame.display.set_caption(settings.window_title)

#frames
clock = pygame.time.Clock()

running = True

#Object Creation

r = Renderer()
c = Camera()

cba = CombatArea(0, 1100, 200, 800)

player = Player()

platform = Platform(200, 500, 30, 400, 0, 40)
platforms = [platform]

wall = Wall(200, 500, 0, 400, 30, 40)
walls = [wall]

slope = Slope(700, 500, 0, 100, 80, 200)
slope2 = Slope(500, 400, 50, 100, 50, 200, direction=-1)
slopes = [slope, slope2]

enemy = Enemy("basic", 400, 300, behavior="opportunist")
enemy2 = Enemy("fast", 500, 300)
enemy3 = Enemy("heavy", 600, 300, behavior="opportunist")
enemy4 = Enemy("fast", 400, 600)
enemy5 = Enemy("basic", 500, 600, z=0, boss=True)
enemy6 = Enemy("heavy", 600, 600)
enemy7 = Enemy("basic", 700, 450)
enemy8 = Enemy("basic", 900, 300)
enemy9 = Enemy("heavy", 900, 600)
enemies = [enemy, enemy2, enemy3, enemy4, enemy5, enemy6, enemy7, enemy8, enemy9]

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
    player.update(keys, dt, platforms, walls, slopes, enemies)
    c.update(player, dt)

    #enemy updates
    for enemy in enemies:
        other_enemies = []
        for other in enemies:
            if other != enemy:
                other_enemies.append(other)

        enemy.update(dt, player, walls, other_enemies, slopes, cba)

    surviving = []
    for enemy in enemies:
        if enemy.alive:
            surviving.append(enemy)

    enemies = surviving

    # Build environment

    r.draw_scene(screen, player, platforms, walls, enemies, slopes, c.x)

    if player.currently_attacking:
        atk_hitbox = player.get_attack_hitbox()

        player.draw_attack(screen, atk_hitbox, c.x)

        for enemy in enemies:
            if enemy.invuln_t <= 0 and enemy.check_col(atk_hitbox):
                enemy.been_hit = True
                enemy.health -= 25
                enemy.invuln_t = enemy.invuln_dur

                enemy.receive_hit(player.attack_direction)
    
    for enemy in enemies:
        if enemy.alive:
            atk_hitbox = enemy.get_attack_hitbox()
            enemy.draw_attack_hitbox(screen, c.x)

            if atk_hitbox is not None:
                if enemy.current_attack != "charge":
                    if player.invuln_t <= 0 and player.check_col(atk_hitbox):
                        player.take_damage(enemy.attack_damage)

    if not player.alive:
        death_text = death_font.render("YOU DIED", True, (220, 30, 30))
        death_rect = death_text.get_rect(center=(settings.screen_width // 2, settings.screen_height // 2))
        screen.blit(death_text, death_rect)

    #display update
    pygame.display.flip()


pygame.quit()
import pygame
import settings
from src.Player.player import Player
from src.Environment.platform import Platform
from src.Environment.wall import Wall
pygame.init()

#window
screen = pygame.display.set_mode(
    (settings.screen_width, settings.screen_height)
)

pygame.display.set_caption(settings.window_title)

#frames
clock = pygame.time.Clock()

running = True

test_player = Player()
test_platform1 = Platform(100, 100, 60, 200, 20, 100)
test_platform2 = Platform(310, 100, 50, 200, 20, 100)
platforms = [test_platform1,test_platform2]

test_wall1 = Wall(300, 200, 0, 50, 50, 50)
test_wall2 = Wall(400, 400, 0, 50, 100, 50)
walls = [test_wall1, test_wall2]
while running:

    #event handler
    for event in pygame.event.get():

        #player closes window 
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                test_player.jump()

    #Fps step
    dt = clock.tick(settings.fps) / 1000

    #background
    screen.fill(settings.bg_color)

    #Character Controls
    keys = pygame.key.get_pressed()
    test_player.update(keys, dt, platforms, walls)

    for platform in platforms:
        platform.draw(screen)

    for wall in walls:
        wall.draw(screen)

    test_player.draw(screen)

    #display update
    pygame.display.flip()



pygame.quit()
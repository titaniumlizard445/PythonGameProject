import pygame
import settings
from src.Player.player import Player
from src.Environment.platform import Platform
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
test_platform = Platform(100, 100, 60, 200, 20, 100)
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
    test_player.update(keys, dt, test_platform,)

    test_platform.draw(screen)
    test_player.draw(screen)

    #display update
    pygame.display.flip()



pygame.quit()
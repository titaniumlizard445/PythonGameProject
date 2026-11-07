import pygame
import settings
from src.Player.player import Player

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

while running:

    #event handler
    for event in pygame.event.get():

        #player closes window
        if event.type == pygame.QUIT:
            running = False

    #Fps step
    dt = clock.tick(settings.fps) / 1000

    #background
    screen.fill(settings.bg_color)

    #Character Controls
    keys = pygame.key.get_pressed()
    test_player.update(keys, dt)

    test_player.draw(screen)

    #display update
    pygame.display.flip()



pygame.quit()
#Contains camera and drawing preferences

import settings

class Camera:

    def __init__(self):
        self.x = 0

        self.follow_speed = 5
        self.offset_x = 0


    def update(self, player, dt):
        target_x = player.x - settings.screen_width / 2

        difference = target_x - self.x
        self.x += difference * min(1, self.follow_speed * dt)
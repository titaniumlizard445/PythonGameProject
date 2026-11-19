
# controls rendering

from src.Environment.wall import Wall


class Renderer:

    def draw_shadow(self, screen, player, platforms, walls):
        player.draw_shadow(screen, platforms)

        self.draw_occluding_walls(screen, player, walls, Wall.covers_shadow, platforms)

    def draw_player(self, screen, player, walls):
        player.draw(screen)

        self.draw_occluding_walls(screen, player, walls, Wall.covers_player)

    def draw_scene(self, screen, player, platforms, walls, enemies):
        draw_queue = []

        for platform in platforms:
            draw_queue.append((platform.depth_sort, 1, lambda p=platform: p.draw(screen)))

        for wall in walls:
            draw_queue.append((wall.side_depth, 1, lambda w=wall: w.draw_side(screen)))

            draw_queue.append((wall.front_depth, 1, lambda w=wall: w.draw_front(screen)))

        for enemy in enemies:
            draw_queue.append((enemy.depth_sort, 1, lambda e=enemy: e.draw(screen)))

        # Draw environment in depth order
        draw_queue.sort(key=lambda item: (item[0], item[1]))

        for _, _, draw_function in draw_queue:
            draw_function()

        # Draw shadow and player, including wall occlusion
        self.draw_shadow(screen, player, platforms, walls)
        self.draw_player(screen, player, walls)

    def draw_occluding_walls(self, screen, player, walls, check_method, *args):
        for wall in walls:
            if check_method(wall, player, *args):
                wall.draw_front(screen)
                wall.draw_side(screen)
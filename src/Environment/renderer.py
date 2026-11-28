# controls rendering

class Renderer:

    def draw_shadow(self, screen, player, platforms, walls, slopes, camera_x):
        player.draw_shadow(screen, platforms, slopes, camera_x)

        self.draw_occluding_walls(screen, player, player.get_shadow_bounds(platforms, slopes, camera_x), walls, camera_x)


    def draw_player(self, screen, player, walls, camera_x):
        player.draw(screen, camera_x)

        self.draw_occluding_walls(screen, player, player.get_vis_bounds(camera_x), walls, camera_x)


    def draw_scene(self, screen, player, platforms, walls, enemies, slopes, camera_x):
        draw_queue = []

        for platform in platforms:
            platform_sort = platform.depth_sort

            if player.z >= platform.z:
                platform_sort = min(platform_sort, player.depth_sort - 0.001)

            draw_queue.append((platform_sort, 1, lambda p=platform: p.draw(screen, camera_x)))

        for slope in slopes:
            slope_sort = slope.y - slope.d / 2

            if slope.overlaps_player(player) and player.z >= slope.get_player_surface_height(player):
                slope_sort = player.depth_sort - 0.001

            for enemy in enemies:
                if slope.overlaps_player(enemy) and enemy.z >= slope.get_player_surface_height(enemy):
                    slope_sort = min(slope_sort, enemy.depth_sort - 0.001)

            draw_queue.append((slope_sort, 1, lambda s=slope: s.draw(screen, camera_x)))

        for wall in walls:
            draw_queue.append((wall.front_depth, 1, lambda w=wall: w.draw_front(screen, camera_x)))

        for enemy in enemies:
            draw_queue.append((enemy.depth_sort, 1, lambda e=enemy: e.draw(screen, camera_x)))
            draw_queue.append((enemy.depth_sort, 2, lambda e=enemy: e.draw_position_target(screen, camera_x)))

        
        draw_queue.append((player.depth_sort, 0, lambda: self.draw_shadow(screen, player, platforms, walls, slopes, camera_x)))

        
        draw_queue.append((player.depth_sort, 1, lambda: self.draw_player(screen, player, walls, camera_x)))

        
        draw_queue.sort(key=lambda item: (item[0], item[1]))

        for _, _, draw_function in draw_queue:
            draw_function()

        


    def draw_occluding_walls(self, screen, player, bounds, walls, camera_x):
        for wall in walls:
            surface = wall.get_front_surface()
            clip_rect = self.get_surf_over_rect(surface, bounds, camera_x)
            old_clip = screen.get_clip()

            if clip_rect is not None and self.get_pl_depth_state(surface, player) == "behind":
                screen.set_clip(clip_rect)
                surface.draw(screen, camera_x)

            screen.set_clip(old_clip)


    def surface_overlap_bounds(self, surface, bounds, camera_x=0):
        s_bounds = surface.get_scrn_bounds(camera_x)

        if 0 < (min(s_bounds[0][1], bounds[1]) - max(s_bounds[0][0], bounds[0])):
            if 0 < (min(s_bounds[1][1], bounds[3]) - max(s_bounds[1][0], bounds[2])):
                return True

        return False


    def get_surf_over_rect(self, surface, bounds, camera_x=0):
        if not self.surface_overlap_bounds(surface, bounds, camera_x):
            return None
        
        s_bounds = surface.get_scrn_bounds(camera_x)

        x_min = max(s_bounds[0][0], bounds[0])
        x_max = min(s_bounds[0][1], bounds[1])
        y_min = max(s_bounds[1][0], bounds[2])
        y_max = min(s_bounds[1][1], bounds[3])

        rect = (x_min, y_min, x_max - x_min, y_max - y_min)
        return rect


    def get_pl_depth_state(self, surface, player):
        if player.y - player.depth / 2 < surface.y:
            return "behind"
        elif player.y - player.depth / 2 > surface.y:
            return "front"
        else:
            return "straddling"
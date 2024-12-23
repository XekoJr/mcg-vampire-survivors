from enemies.enemy import Enemy
import pygame
import math
from projectile import boss_projectiles, boss_projectile_frames

class Boss1Enemy(Enemy):
    """Boss enemy with unique behaviors."""
    def __init__(self, x, y):
        images = [
            pygame.image.load(f'./assets/images/enemies/boss_1/{i}.png') for i in range(26)
        ]
        super().__init__(x, y, hp=500, speed=1, xp_value=200, damage=60, size=(150, 150), images=images)
        self.shoot_interval = 1000 
        self.first_shot_delay = 125
        self.last_shot_time = pygame.time.get_ticks() + self.first_shot_delay


    def shoot_at_player(self, player):
        """Shoot a projectile towards the player's position."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.shoot_interval:
            # Calculate direction
            dx = player.x + player.size / 2 - (self.x + self.size[0] / 2)
            dy = player.y + player.size / 2 - (self.y + self.size[1] / 2)
            distance = math.sqrt(dx ** 2 + dy ** 2)
            if distance > 0:
                dx /= distance
                dy /= distance

            # Calculate angle for projectile rotation
            angle = math.degrees(math.atan2(-dy, dx))

            # Append new projectile
            boss_projectiles.append({
                'x': self.x + self.size[0] / 2,
                'y': self.y + self.size[1] / 2,
                'dx': dx,
                'dy': dy,
                'damage': self.damage,
                'speed': 5,
                'frames': boss_projectile_frames,
                'frame_index': 0,
                'last_frame_time': pygame.time.get_ticks(),
                'angle': angle
            })

            self.last_shot_time = current_time
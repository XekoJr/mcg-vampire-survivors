import pygame
from enemies.__init__ import BatEnemy, BlobEnemy, SkeletonEnemy
from settings import MAP_WIDTH, MAP_HEIGHT, normal_hit_sound, crit_hit_sound
import random

class EnemyManager:
    """Manages all enemy-related logic."""
    def __init__(self):
        self.enemies = []
        self.spawn_timer = 0
        self.base_spawn_interval = 140  # Base spawn interval (frames)
        self.spawn_interval = self.base_spawn_interval
        self.level_enemy_map = {
            1: {"enemies": [(BatEnemy, 1)]},  # Only bats with weight 1
            2: {"enemies": [(BatEnemy, 3), (SkeletonEnemy, 1)]},  # Bats are more common
            3: {"enemies": [(BatEnemy, 2), (SkeletonEnemy, 2), (BlobEnemy, 1)]},  # More variety
            4: {"enemies": [(BatEnemy, 3), (SkeletonEnemy, 3), (BlobEnemy, 2)]},  # More blobs
            5: {"enemies": [(BatEnemy, 1), (SkeletonEnemy, 1), (BlobEnemy, 1)]},  # Eazy Boss
            10: {"enemies": [(BatEnemy, 2), (SkeletonEnemy, 2), (BlobEnemy, 2)]}, # Medium Boss
            15: {"enemies": [(BatEnemy, 3), (SkeletonEnemy, 3), (BlobEnemy, 3)]}, # Hard Boss
        }

    def update_spawn_interval(self, player_level):
        """Update the spawn interval based on the player's level."""
        self.spawn_interval = max(30, self.base_spawn_interval - (player_level * 5))

    def spawn_enemy(self, player_level):
        """Spawn a new enemy based on the player's level."""
        if player_level not in self.level_enemy_map:
            player_level = max(self.level_enemy_map.keys())  # Cap at highest level configuration

        self.update_spawn_interval(player_level)  # Update spawn interval based on level

        level_config = self.level_enemy_map[player_level]
        enemy_types = level_config["enemies"]

        # Weighted random choice based on spawn weights
        enemy_type = random.choices(
            [etype for etype, _ in enemy_types], 
            weights=[weight for _, weight in enemy_types],
            k=1
        )[0]

        # Randomly choose a side for spawning
        side = random.randint(0, 3)
        if side == 0:  # Top edge
            x, y = random.randint(0, MAP_WIDTH - 50), -50
        elif side == 1:  # Bottom edge
            x, y = random.randint(0, MAP_WIDTH - 50), MAP_HEIGHT
        elif side == 2:  # Left edge
            x, y = -50, random.randint(0, MAP_HEIGHT - 50)
        else:  # Right edge
            x, y = MAP_WIDTH, random.randint(0, MAP_HEIGHT - 50)

        # Spawn the chosen enemy
        self.enemies.append(enemy_type(x, y))

    def update_enemies(self, player_x, player_y):
        """Update the position of all enemies."""
        for enemy in self.enemies:
            enemy.move_toward_player(player_x, player_y)

    def draw_enemies(self, screen, camera_x, camera_y):
        """Draw all enemies on the screen."""
        for enemy in self.enemies:
            enemy.draw(screen, camera_x, camera_y)

    def handle_projectile_collisions(self, projectiles, player, xp_drops):
        """Check for collisions between projectiles and enemies."""
        for projectile in projectiles[:]:
            projectile_rect = pygame.Rect(projectile['x'], projectile['y'], 10, 10)

            for enemy in self.enemies[:]:
                if projectile_rect.colliderect(enemy.get_rect()):
                    # Play the appropriate sound effect
                    if projectile['is_crit'] and crit_hit_sound:
                        crit_hit_sound.play()
                    elif normal_hit_sound:
                        normal_hit_sound.play()

                    # Handle damage
                    if enemy.take_damage(projectile['damage']):  # Enemy dies
                        self.enemies.remove(enemy)
                        player.score += 10
                        xp_drops.append({
                            'x': enemy.x, 
                            'y': enemy.y,
                            'value': enemy.xp_value  # XP value depends on the enemy
                            })  # Drop XP
                    projectiles.remove(projectile)
                    break

    def handle_player_collisions(self, player):
        """Check for collisions between the player and enemies."""
        player_rect = pygame.Rect(player.x, player.y, player.size, player.size)
        for enemy in self.enemies[:]:
            if player_rect.colliderect(enemy.get_rect()):
                # Apply the enemy's damage to the player
                player.health -= enemy.damage
                self.enemies.remove(enemy)  # Remove the enemy after collision
                return True  # Collision occurred
        return False  # No collision

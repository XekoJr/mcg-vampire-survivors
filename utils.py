import pygame
from settings import *
from projectile import projectiles
from xp import xp_drops

def check_projectile_collisions(player, enemy_manager):
    """Handle collisions between projectiles and enemies."""
    for projectile in projectiles[:]:
        projectile_rect = pygame.Rect(projectile['x'], projectile['y'], 10, 10)

        for enemy in enemy_manager.enemies[:]:
            if projectile_rect.colliderect(enemy.get_rect()):
                # Reduce enemy HP by projectile damage
                if enemy.take_damage(projectile['damage']):
                    # If enemy dies, remove it and drop XP
                    enemy_manager.enemies.remove(enemy)
                    player.score += 10
                    xp_drops.append({'x': enemy.x, 'y': enemy.y})  # Drop XP
                
                # Remove the projectile after collision
                projectiles.remove(projectile)
                break  # Exit loop after handling collision

def check_player_collisions(player, enemy_manager):
    """Check for collisions between the player and enemies."""
    player_rect = pygame.Rect(player.x, player.y, player.size, player.size)
    for enemy in enemy_manager.enemies[:]:
        if player_rect.colliderect(enemy.get_rect()):
            # Remove enemy upon collision
            enemy_manager.enemies.remove(enemy)
            return True
    return False

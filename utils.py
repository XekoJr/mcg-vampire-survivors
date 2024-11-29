import pygame
from settings import *
from enemy import enemies
from projectile import projectiles
from xp import xp_drops

def check_projectile_collisions(player):
    """Handle collisions between projectiles and enemies."""
    for projectile in projectiles[:]:
        projectile_rect = pygame.Rect(projectile['x'], projectile['y'], 10, 10)

        for enemy in enemies[:]:
            enemy_rect = pygame.Rect(enemy['x'], enemy['y'], 50, 70)
            if projectile_rect.colliderect(enemy_rect):
                # Reduce enemy HP by projectile damage
                enemy['hp'] -= projectile['damage']

                # Check if enemy dies
                if enemy['hp'] <= 0:
                    enemies.remove(enemy)
                    player.score += 10  # Award score
                    xp_drops.append({'x': enemy['x'], 'y': enemy['y']})  # Drop XP

                # Remove the projectile after collision
                projectiles.remove(projectile)
                break

def check_player_collisions(player):
    player_rect = pygame.Rect(player.x, player.y, player.size, player.size)
    for enemy in enemies[:]:
        enemy_rect = pygame.Rect(enemy['x'], enemy['y'], 50, 70)
        if player_rect.colliderect(enemy_rect):
            enemies.remove(enemy)
            return True
    return False

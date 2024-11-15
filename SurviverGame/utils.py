import pygame
from settings import *
from enemy import enemies
from projectile import projectiles
from xp import xp_drops

def check_projectile_collisions(player):
    for projectile in projectiles[:]:
        projectile_rect = pygame.Rect(projectile['x'], projectile['y'], 10, 10)
        for enemy in enemies[:]:
            enemy_rect = pygame.Rect(enemy['x'], enemy['y'], 40, 40)
            if projectile_rect.colliderect(enemy_rect):
                enemies.remove(enemy)
                projectiles.remove(projectile)
                player.score += 10
                xp_drops.append({'x': enemy['x'], 'y': enemy['y']})
                break

def check_player_collisions(player):
    player_rect = pygame.Rect(player.x, player.y, player.size, player.size)
    for enemy in enemies[:]:
        enemy_rect = pygame.Rect(enemy['x'], enemy['y'], 40, 40)
        if player_rect.colliderect(enemy_rect):
            enemies.remove(enemy)
            return True
    return False

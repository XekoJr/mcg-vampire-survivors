import pygame
from settings import *
import math

projectiles = []

def fire_projectile(player):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dx = mouse_x - (player.x + player.size / 2)
    dy = mouse_y - (player.y + player.size / 2)
    distance = math.sqrt(dx ** 2 + dy ** 2)
    if distance != 0:
        dx /= distance
        dy /= distance
    projectiles.append({'x': player.x + player.size // 2, 'y': player.y + player.size // 2, 'dx': dx, 'dy': dy})

def move_projectiles():
    for projectile in projectiles[:]:
        projectile['x'] += projectile['dx'] * projectile_speed
        projectile['y'] += projectile['dy'] * projectile_speed
        if projectile['x'] < 0 or projectile['x'] > WIDTH or projectile['y'] < 0 or projectile['y'] > HEIGHT:
            projectiles.remove(projectile)

def draw_projectiles(screen):
    for projectile in projectiles:
        pygame.draw.rect(screen, YELLOW, (projectile['x'], projectile['y'], 10, 10))

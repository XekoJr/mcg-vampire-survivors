import random
import pygame
from settings import *
import math

# List to store active projectiles
projectiles = []

def fire_projectile(player, camera_x, camera_y):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dx = mouse_x + camera_x - (player.x + player.size / 2)
    dy = mouse_y + camera_y - (player.y + player.size / 2)
    distance = math.sqrt(dx ** 2 + dy ** 2)
    if distance != 0:
        dx /= distance
        dy /= distance

    is_crit = random.random() < (player.crit_chance / 100)
    damage = player.projectile_damage * 2 if is_crit else player.projectile_damage

    projectiles.append({
        'x': player.x + player.size / 2,
        'y': player.y + player.size / 2,
        'dx': dx,
        'dy': dy,
        'damage': damage,
        'color': RED if is_crit else YELLOW
    })

def move_projectiles():
    """Update the position of all projectiles."""
    for projectile in projectiles[:]:
        projectile['x'] += projectile['dx'] * projectile_speed  # Move x
        projectile['y'] += projectile['dy'] * projectile_speed  # Move y

        # Remove projectiles that go out of map boundaries
        if (projectile['x'] < 0 or projectile['x'] > MAP_WIDTH or
                projectile['y'] < 0 or projectile['y'] > MAP_HEIGHT):
            projectiles.remove(projectile)


def draw_projectiles(screen, camera_x, camera_y):
    """Draw all projectiles relative to the camera."""
    for projectile in projectiles:
        pygame.draw.rect(screen, projectile['color'], (
            projectile['x'] - camera_x,  # Adjust for camera offset
            projectile['y'] - camera_y,
            10, 10  # Projectile size
        ))

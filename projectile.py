import pygame
from settings import *
import math

projectiles = []

def fire_projectile(player, camera_x, camera_y):
    # Get mouse position in the world
    mouse_x, mouse_y = pygame.mouse.get_pos()
    world_mouse_x = mouse_x + camera_x
    world_mouse_y = mouse_y + camera_y

    # Calculate direction
    dx = world_mouse_x - (player.x + player.size / 2)
    dy = world_mouse_y - (player.y + player.size / 2)
    distance = math.sqrt(dx ** 2 + dy ** 2)
    if distance != 0:  # Normalize direction
        dx /= distance
        dy /= distance

    # Add projectile to the list
    projectiles.append({
        'x': player.x + player.size / 2,
        'y': player.y + player.size / 2,
        'dx': dx,
        'dy': dy
    })

def move_projectiles():
    for projectile in projectiles[:]:
        projectile['x'] += projectile['dx'] * projectile_speed
        projectile['y'] += projectile['dy'] * projectile_speed

        # Remove projectiles that move outside the map boundaries
        if (projectile['x'] < 0 or projectile['x'] > MAP_WIDTH or
                projectile['y'] < 0 or projectile['y'] > MAP_HEIGHT):
            projectiles.remove(projectile)

def draw_projectiles(screen, camera_x, camera_y):
    """Draws all projectiles relative to the camera."""
    for projectile in projectiles:
        pygame.draw.rect(screen, YELLOW, (
            projectile['x'] - camera_x,
            projectile['y'] - camera_y,
            10, 10
        ))


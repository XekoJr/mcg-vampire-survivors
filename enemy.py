import pygame
import random
import math
from settings import *

enemies = []

def spawn_enemy():
    # Randomly choose a side: 0 = top, 1 = bottom, 2 = left, 3 = right
    side = random.randint(0, 3)

    if side == 0:  # Top edge
        x = random.randint(0, MAP_WIDTH - 40)
        y = -40
    elif side == 1:  # Bottom edge
        x = random.randint(0, MAP_WIDTH - 40)
        y = MAP_HEIGHT
    elif side == 2:  # Left edge
        x = -40
        y = random.randint(0, MAP_HEIGHT - 40)
    else:  # Right edge
        x = MAP_WIDTH
        y = random.randint(0, MAP_HEIGHT - 40)

    # Add the new enemy to the list
    enemies.append({'x': x, 'y': y})

def draw_enemies(screen, camera_x, camera_y):
    for enemy in enemies:
        pygame.draw.rect(screen, RED, (
            enemy['x'] - camera_x,
            enemy['y'] - camera_y,
            40, 40
        ))


def move_enemies(player_x, player_y):
    for enemy in enemies:
        dx = player_x - enemy['x']
        dy = player_y - enemy['y']
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 0:
            dx /= distance
            dy /= distance
        enemy['x'] += dx
        enemy['y'] += dy

import pygame
import random
import math
from settings import *

enemies = []

def spawn_enemy():
    side = random.randint(0, 3)
    if side == 0:
        x = random.randint(0, WIDTH - 40)
        y = -40
    elif side == 1:
        x = random.randint(0, WIDTH - 40)
        y = HEIGHT
    elif side == 2:
        x = -40
        y = random.randint(0, HEIGHT - 40)
    else:
        x = WIDTH
        y = random.randint(0, HEIGHT - 40)
    enemies.append({'x': x, 'y': y})

def draw_enemies(screen):
    for enemy in enemies:
        pygame.draw.rect(screen, RED, (enemy['x'], enemy['y'], 40, 40))

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

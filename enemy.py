import pygame
import random
import math
from settings import *

# Global variables for animation
enemies = []
enemy_animation_index = 0  # Current animation frame
enemy_animation_timer = 0  # Timer to control animation frame switching

# Load and resize enemy images
enemy_images = [
    pygame.image.load('./images/enemies/bat/0.png'),
    pygame.image.load('./images/enemies/bat/1.png'),
    pygame.image.load('./images/enemies/bat/2.png'),
    pygame.image.load('./images/enemies/bat/3.png')
]
enemy_images = [pygame.transform.scale(image, ENEMY_SIZE) for image in enemy_images]

def spawn_enemy():
    """Spawn an enemy at a random position along the screen edge."""
    side = random.randint(0, 3)
    if side == 0:  # Top edge
        x = random.randint(0, MAP_WIDTH - ENEMY_SIZE[0])
        y = -ENEMY_SIZE[1]
    elif side == 1:  # Bottom edge
        x = random.randint(0, MAP_WIDTH - ENEMY_SIZE[0])
        y = MAP_HEIGHT
    elif side == 2:  # Left edge
        x = -ENEMY_SIZE[0]
        y = random.randint(0, MAP_HEIGHT - ENEMY_SIZE[1])
    else:  # Right edge
        x = MAP_WIDTH
        y = random.randint(0, MAP_HEIGHT - ENEMY_SIZE[1])

    enemy_hp = 20  # Starting HP for enemies
    enemies.append({'x': x, 'y': y, 'hp': enemy_hp})

def draw_enemies(screen, camera_x, camera_y):
    """Draw enemies and their health bars."""
    global enemy_animation_index, enemy_animation_timer

    # Update animation frame
    enemy_animation_timer += 1
    if enemy_animation_timer >= 5:
        enemy_animation_index = (enemy_animation_index + 1) % len(enemy_images)
        enemy_animation_timer = 0

    for enemy in enemies:
        max_hp = 20  # Maximum HP for scaling
        health_ratio = max(0, enemy['hp'] / max_hp)

        # Draw the HP bar
        pygame.draw.rect(screen, BLACK, (
            enemy['x'] - camera_x,
            enemy['y'] - camera_y - 10,  # Position above enemy
            ENEMY_SIZE[0], 5  # Match enemy width
        ))
        pygame.draw.rect(screen, GREEN if health_ratio > 0.6 else YELLOW if health_ratio > 0.3 else RED, (
            enemy['x'] - camera_x,
            enemy['y'] - camera_y - 10,
            ENEMY_SIZE[0] * health_ratio, 5
        ))

        # Draw the enemy image
        screen.blit(enemy_images[enemy_animation_index], (
            enemy['x'] - camera_x,
            enemy['y'] - camera_y
        ))

def move_enemies(player_x, player_y):
    """Move enemies toward the player."""
    for enemy in enemies:
        dx = player_x - enemy['x']
        dy = player_y - enemy['y']
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 0:
            dx /= distance
            dy /= distance
        enemy['x'] += dx
        enemy['y'] += dy

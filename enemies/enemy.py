import pygame
from settings import *
import math

class Enemy:
    """Base class for all enemies."""
    def __init__(self, x, y, hp, speed, xp_value, damage, size, images):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = hp  # Store the maximum HP for the health ratio
        self.speed = speed
        self.xp_value = xp_value  # XP value when the enemy dies
        self.damage =  damage
        self.size = size
        self.images = [pygame.transform.scale(img, self.size) for img in images]
        self.animation_index = 0
        self.animation_timer = 0

    def move_toward_player(self, player_x, player_y):
        """Move the enemy toward the player."""
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 0:
            dx /= distance
            dy /= distance
        self.x += dx * self.speed
        self.y += dy * self.speed

    def take_damage(self, damage):
        """Reduce health and return True if the enemy dies."""
        self.hp -= damage
        return self.hp <= 0

    def draw(self, screen, camera_x, camera_y):
        """Draw the enemy and its HP bar."""
        # Update animation frame
        self.animation_timer += 1
        if self.animation_timer >= 10:
            self.animation_index = (self.animation_index + 1) % len(self.images)
            self.animation_timer = 0

        # Draw the enemy sprite
        screen.blit(self.images[self.animation_index], (
            self.x - camera_x,
            self.y - camera_y
        ))

        # Draw the HP bar above the enemy
        health_ratio = max(0, self.hp / self.max_hp)  # Ensure ratio is never below 0
        pygame.draw.rect(screen, BLACK, (
            self.x - camera_x,
            self.y - camera_y - 10,  # Position above the enemy
            self.size[0], 5  # Match enemy width
        ))
        pygame.draw.rect(screen, GREEN if health_ratio > 0.6 else YELLOW if health_ratio > 0.3 else RED, (
            self.x - camera_x,
            self.y - camera_y - 10,
            self.size[0] * health_ratio, 5  # Scale width based on health ratio
        ))

    def get_rect(self):
        """Get the enemy's collision rectangle."""
        return pygame.Rect(self.x, self.y, self.size[0], self.size[1])

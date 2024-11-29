import pygame
from settings import *

class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.size = 50
        self.speed = 2
        self.health = 100
        self.xp = 0  # Total XP collected
        self.level = 1  # Starting level
        self.current_xp = 0  # XP toward the next level
        self.xp_to_next_level = 50  # Initial XP required to level up
        self.last_shot_time = 0
        self.score = 0
        self.level_up_pending = False

        # Scaling attributes
        self.fire_rate = fire_rate  # Milliseconds between shots
        self.projectile_damage = 10  # Base projectile damage

    def move(self):
        """Update player movement while respecting map boundaries."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y = max(0, self.y - self.speed)  # Top boundary
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y = min(MAP_HEIGHT - self.size, self.y + self.speed)  # Bottom boundary
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x = max(0, self.x - self.speed)  # Left boundary
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x = min(MAP_WIDTH - self.size, self.x + self.speed)  # Right boundary

    def gain_xp(self, amount):
        """Add XP and handle leveling up."""
        self.xp += amount
        self.current_xp += amount

        while self.current_xp >= self.xp_to_next_level:
            self.current_xp -= self.xp_to_next_level
            self.level += 1
            self.xp_to_next_level = round(self.xp_to_next_level * 1.5)
            self.level_up_pending = True  # Set flag to trigger level-up menu
            return True
        return False

    def apply_upgrade(self, upgrade):
        if upgrade == "fire_rate":
            self.fire_rate = max(200, self.fire_rate * 0.8)
        elif upgrade == "damage":
            self.projectile_damage *= 1.2
        elif upgrade == "health":
            max_health = 10  # Define a maximum health value
            self.health = min(max_health, self.health + 1)

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.size, self.size))

    def draw_health(self, screen):
        health_text = font_health.render(f"Health: {self.health}", True, WHITE)
        screen.blit(health_text, (10, 10))

    def draw_score(self, screen):
        score_text = font_score.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (WIDTH - 150, 10))

    def draw_xp(self, screen):
        """Draw XP, Level, and XP Progress."""
        xp_text = font_score.render(f"XP: {self.current_xp}/{self.xp_to_next_level}", True, WHITE)
        level_text = font_score.render(f"Level: {self.level}", True, WHITE)
        screen.blit(xp_text, (10, 40))
        screen.blit(level_text, (10, 70))


    def draw_with_offset(self, screen, camera_x, camera_y):
        pygame.draw.rect(screen, BLUE, (self.x - camera_x, self.y - camera_y, self.size, self.size))

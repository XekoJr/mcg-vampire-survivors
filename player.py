import pygame
import time
import random  # For critical hit calculation
from settings import *

class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.size = 60
        self.speed = 2
        self.health = 100
        self.max_health = 100
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
        self.crit_chance = 0  # Critical hit chance (percentage)

        # Hitbox configuration
        self.hitbox_offset = (10, 10)  # Offset from the sprite's top-left corner
        self.hitbox_size = (40, 40)  # Width and height of the hitbox

        # Player animation
        self.player_images = {
            'down': [pygame.image.load(f'./assets/images/player/down/{i}.png') for i in range(4)],
            'up': [pygame.image.load(f'./assets/images/player/up/{i}.png') for i in range(4)],
            'left': [pygame.image.load(f'./assets/images/player/left/{i}.png') for i in range(4)],
            'right': [pygame.image.load(f'./assets/images/player/right/{i}.png') for i in range(4)],
        }

        # Resize images to the desired size
        self.player_images = {direction: [pygame.transform.scale(image, (self.size, self.size)) for image in images]
                              for direction, images in self.player_images.items()}

        # Animation control variables
        self.animation_index = 0
        self.animation_timer = 0  # Timer to control image switching

        # Initialize player direction (default "down")
        self.direction = 'down'
        self.animation_index = 0

        self.current_image = self.player_images[self.direction][self.animation_index]  # Initial image
        self.last_move_time = time.time()  # Time tracking for animations

        # Control animation speed in seconds
        self.animation_speed = 0.2  # Swap image every 0.2 seconds
        self.last_animation_time = time.time()  # Last animation time

    def get_hitbox(self):
        """Returns the player's hitbox as a pygame.Rect."""
        return pygame.Rect(
            self.x + self.hitbox_offset[0],
            self.y + self.hitbox_offset[1],
            self.hitbox_size[0],
            self.hitbox_size[1]
        )

    def move(self):
        """Update player movement while respecting map boundaries."""
        keys = pygame.key.get_pressed()
        moving = False  # Check if the player is moving

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y = max(0, self.y - self.speed)
            self.direction = 'up'
            moving = True
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y = min(MAP_HEIGHT - self.size, self.y + self.speed)
            self.direction = 'down'
            moving = True
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x = max(0, self.x - self.speed)
            self.direction = 'left'
            moving = True
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x = min(MAP_WIDTH - self.size, self.x + self.speed)
            self.direction = 'right'
            moving = True

        # Update animation only if moving
        if moving:
            current_time = time.time()
            if current_time - self.last_animation_time >= self.animation_speed:
                self.animation_index = (self.animation_index + 1) % len(self.player_images[self.direction])
                self.last_animation_time = current_time
        else:
            self.animation_index = 0  # Reset animation to the first frame when not moving

    def gain_xp(self, amount):
        """Add XP and handle leveling up."""
        self.xp += amount
        self.current_xp += amount

        while self.current_xp >= self.xp_to_next_level:
            self.current_xp -= self.xp_to_next_level
            self.level += 1
            self.xp_to_next_level = round(self.xp_to_next_level * 1.2)
            self.level_up_pending = True  # Set flag to trigger level-up menu
            return True
        return False

    def apply_upgrade(self, upgrade):
        """Apply the chosen upgrade."""
        if upgrade == "fire_rate":
            self.fire_rate = max(200, self.fire_rate * 0.8)  # Faster shooting
        elif upgrade == "damage":
            self.projectile_damage = int(self.projectile_damage * 1.3)  # Increase damage
        elif upgrade == "health":
            self.health = min(self.max_health, self.health + 50)  # Restore health
        elif upgrade == "max_health":
            self.max_health += 25  # Increase max health
            self.health = min(self.max_health, self.health + 25)
        elif upgrade == "speed":
            self.speed += 0.15  # Increase movement speed
        elif upgrade == "crit_chance":
            self.crit_chance = min(100, self.crit_chance + 5)  # Increase crit chance (cap at 100%)

    def draw(self, screen):
        """Draw the player's current animation frame on the screen."""
        screen.blit(self.player_images[self.direction][self.animation_index], (self.x, self.y))

        # Debugging: Draw the hitbox as a rectangle
        pygame.draw.rect(screen, RED, self.get_hitbox(), 1)  # Outline the hitbox in red

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
        """Draw player with camera offset."""
        screen.blit(self.player_images[self.direction][self.animation_index], (self.x - camera_x, self.y - camera_y))

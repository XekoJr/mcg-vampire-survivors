import math
import pygame
import time
import random  # For critical hit calculation
from settings import *

class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.size = 60
        self.speed = 2.5
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

    import math

    def move(self):
        """Update player movement while respecting map boundaries."""
        keys = pygame.key.get_pressed()
        moving = False  # Check if the player is moving

        # Initialize movement deltas
        dx, dy = 0, 0

        # Check for movement in each direction
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -1
            self.direction = 'up'
            moving = True
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = 1
            self.direction = 'down'
            moving = True
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -1
            self.direction = 'left'
            moving = True
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = 1
            self.direction = 'right'
            moving = True

        # Normalize movement for diagonal movement
        magnitude = math.sqrt(dx ** 2 + dy ** 2)
        if magnitude > 0:  # Avoid division by zero
            dx = (dx / magnitude) * self.speed
            dy = (dy / magnitude) * self.speed

        # Apply movement, respecting map boundaries
        self.x = max(0, min(MAP_WIDTH - self.size, self.x + dx))
        self.y = max(0, min(MAP_HEIGHT - self.size, self.y + dy))

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
        """Draw hearts to represent health at the bottom-left corner of the screen."""
        # Load heart images (ensure these are loaded only once)
        if not hasattr(self, 'heart_images'):
            self.heart_images = {
                "empty": pygame.image.load('./assets/images/hp/empty.png'),
                "low": pygame.image.load('./assets/images/hp/low.png'),
                "half": pygame.image.load('./assets/images/hp/half.png'),
                "high": pygame.image.load('./assets/images/hp/high.png'),
                "full": pygame.image.load('./assets/images/hp/full.png')
            }

        # Resize heart images if needed
        heart_size = 32  # Adjust size as necessary
        for key in self.heart_images:
            self.heart_images[key] = pygame.transform.scale(self.heart_images[key], (heart_size, heart_size))

        # Calculate number of hearts based on max HP
        max_hearts = self.max_health // 20
        current_health = self.health
        margin = 10  # Margin from the edges
        spacing = 5  # Space between hearts

        # Position to start drawing hearts
        x = margin
        y = screen.get_height() - margin - heart_size

        # Draw each heart based on the current health
        for i in range(max_hearts):
            if current_health >= 20:
                heart_image = self.heart_images["full"]
            elif current_health >= 15:
                heart_image = self.heart_images["high"]
            elif current_health >= 10:
                heart_image = self.heart_images["half"]
            elif current_health >= 5:
                heart_image = self.heart_images["low"]
            else:
                heart_image = self.heart_images["empty"]

            # Blit the heart image
            screen.blit(heart_image, (x, y))

            # Reduce current health for the next heart
            current_health -= 20

            # Adjust x for the next heart
            x += heart_size + spacing

    def draw_score(self, screen):
        """Draw the player's score in the top-right corner."""
        score_text = font_score.render(f"{self.score}", True, WHITE)
        score_x = screen.get_width() - score_text.get_width() - 20  # Position relative to the right edge
        screen.blit(score_text, (score_x, 25))

    def draw_xp(self, screen):
        """Draw XP bar at the top-center of the screen."""
        # Load the XP bar images (ensure these are loaded only once)
        if not hasattr(self, 'xp_bar_background'):
            self.xp_bar_background = pygame.image.load('./assets/images/xp/xp-bar.png')
            self.xp_bar_green = pygame.image.load('./assets/images/xp/xp.png')

        # Reduce the size of the bars
        original_width = self.xp_bar_background.get_width()
        original_height = self.xp_bar_background.get_height()

        # Scale the bars to 75% of their original size
        scaled_width = int(original_width * 0.75)
        scaled_height = int(original_height * 0.75)

        # Resize the background bar
        xp_bar_background_scaled = pygame.transform.scale(self.xp_bar_background, (scaled_width, scaled_height))

        # Add left and right margin to the green bar
        green_bar_margin = 31.5  # Pixels on both sides
        max_green_width = scaled_width - 2 * green_bar_margin

        # Calculate the XP percentage and determine the green bar's width
        xp_percentage = self.current_xp / self.xp_to_next_level
        green_bar_width = int(max_green_width * xp_percentage)

        # Resize the green bar with adjusted height 
        green_bar_height = int(scaled_height * 0.475)  # Make the green bar 50% of the background's height
        xp_bar_green_scaled = pygame.transform.scale(self.xp_bar_green, (green_bar_width, green_bar_height))

        # Calculate the top-center position for the bars
        screen_width = screen.get_width()
        bar_x = (screen_width - scaled_width) // 2
        bar_y = 20  # Small margin from the top

        # Draw the grey background bar
        screen.blit(xp_bar_background_scaled, (bar_x, bar_y))

        # Center the green bar vertically within the grey background
        green_bar_y = bar_y + (scaled_height - green_bar_height) // 2

        # Draw the green bar on top, respecting the margin
        screen.blit(xp_bar_green_scaled, (bar_x + green_bar_margin, green_bar_y))

    def draw_with_offset(self, screen, camera_x, camera_y):
        """Draw player with camera offset."""
        screen.blit(self.player_images[self.direction][self.animation_index], (self.x - camera_x, self.y - camera_y))

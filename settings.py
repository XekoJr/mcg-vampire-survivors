# settings.py

import pygame  # Import pygame to define fonts and colors

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
RED = (200, 0, 0)
DARK_RED = (150, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Button dimensions
button_width, button_height = 200, 50
button_x = (WIDTH - button_width) // 2
button_y = HEIGHT // 2

# Game settings
player_speed = 2
projectile_speed = 7
fire_rate = 20
enemy_spawn_rate = 30
xp_value = 5  # XP points per drop

# Font settings (after pygame is initialized in main.py)
font_title = pygame.font.Font(pygame.font.match_font('arial'), 50)
font_button = pygame.font.Font(pygame.font.match_font('arial'), 30)
font_credit = pygame.font.Font(pygame.font.match_font('arial'), 20)
font_health = pygame.font.Font(pygame.font.match_font('arial'), 25)
font_score = pygame.font.Font(pygame.font.match_font('arial'), 25)

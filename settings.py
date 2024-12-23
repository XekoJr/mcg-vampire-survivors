# settings.py

import pygame  # Import pygame to define fonts and colors

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Game world size (map limits)
MAP_WIDTH = 1920
MAP_HEIGHT = 1080

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

# Enemy settings
ENEMY_SIZE = (50, 40)  # Width and height of the enemy

# Game settings
player_speed = 2 # Speed of the player character
projectile_speed = 7 # Speed of player projectiles
fire_rate = 1000 # Milliseconds between shots
enemy_spawn_rate = 50 # Lower value means faster spawn rate

# Font settings (after pygame is initialized in main.py)
font_title = pygame.font.Font(pygame.font.match_font('arial'), 50)
font_button = pygame.font.Font(pygame.font.match_font('arial'), 30)
font_credit = pygame.font.Font(pygame.font.match_font('arial'), 20)
font_health = pygame.font.Font(pygame.font.match_font('arial'), 25)
font_score = pygame.font.Font(pygame.font.match_font('arial'), 25)



# Audio settings
pygame.mixer.init()  # Initialize the pygame mixer

# Sound effects
try:
    # Music
    main_menu_music = pygame.mixer.Sound('./assets/audio/main-menu-music.wav')
    game_music = pygame.mixer.Sound('./assets/audio/ingame-music.wav')

    # Sound effects
    normal_hit_sound = pygame.mixer.Sound('./assets/audio/normal-hit.wav')
    crit_hit_sound = pygame.mixer.Sound('./assets/audio/crit-hit.wav')
    collect_xp_sound = pygame.mixer.Sound('./assets/audio/xp-collect.wav')
    level_up_sound = pygame.mixer.Sound('./assets/audio/level-up.wav')

    # Set default volume for sounds
    main_menu_music.set_volume(0.1)
    game_music.set_volume(0.1)
    normal_hit_sound.set_volume(1.0)
    crit_hit_sound.set_volume(1.0)
    collect_xp_sound.set_volume(0.5)
    level_up_sound.set_volume(1.0)

except pygame.error as e:
    print(f"Error loading sounds: {e}")
    normal_hit_sound, crit_hit_sound, collect_xp_sound, level_up_sound = None, None, None, None
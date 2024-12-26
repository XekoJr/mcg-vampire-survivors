# settings.py

import pygame  # Import pygame to define fonts and colors

# Screen dimensions
WIDTH, HEIGHT = 1366, 768

# Game world size (map limits)
MAP_WIDTH = 3000
MAP_HEIGHT = 3000

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
DARK_GRAY = (169, 169, 169)
RED = (200, 0, 0)
DARK_RED = (150, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 0)
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
    hurt_sound = pygame.mixer.Sound('./assets/audio/hurt.wav')

    # Set default volume for sounds
    main_menu_music.set_volume(0.1)
    game_music.set_volume(0.1)
    normal_hit_sound.set_volume(0.5)
    crit_hit_sound.set_volume(0.6)
    collect_xp_sound.set_volume(0.5)
    level_up_sound.set_volume(0.5)

except pygame.error as e:
    print(f"Error loading sounds: {e}")
    main_menu_music = None
    game_music = None
    
    normal_hit_sound = None
    crit_hit_sound = None
    collect_xp_sound = None
    level_up_sound = None
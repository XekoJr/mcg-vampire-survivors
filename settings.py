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
    boss_music = pygame.mixer.Sound('./assets/audio/boss-music.wav')           

    # Menu Interaction
    hover_sound = pygame.mixer.Sound('./assets/audio/menu-hover.wav')          
    click_sound = pygame.mixer.Sound('./assets/audio/menu-click.wav')          

    # Sound effects
        # Projectile sounds
    normal_hit_sound = pygame.mixer.Sound('./assets/audio/normal-hit.wav')    
    crit_hit_sound = pygame.mixer.Sound('./assets/audio/crit-hit.wav')        

        # xp and level up sounds
    collect_xp_sound = pygame.mixer.Sound('./assets/audio/xp-collect.wav')    
    level_up_sound = pygame.mixer.Sound('./assets/audio/level-up.wav')        

        # Player sounds
    hurt_sound = pygame.mixer.Sound('./assets/audio/hurt.wav')               
    death_sound = pygame.mixer.Sound('./assets/audio/death/player-death.wav')
        
        # Ability sounds
    ability_obtained_sound = pygame.mixer.Sound('./assets/audio/ability-obtained.wav') #todo
    ability_used_sound = pygame.mixer.Sound('./assets/audio/ability-used.wav')         #todo

        # Enemy sounds
    bat_death_sound = pygame.mixer.Sound('./assets/audio/death/bat-death.wav')
    skeleton_death_sound = pygame.mixer.Sound('./assets/audio/death/skeleton-death.wav')
    blob_death_sound = pygame.mixer.Sound('./assets/audio/death/blob-death.wav')
    boss_death_sound = pygame.mixer.Sound('./assets/audio/death/boss-death.wav')
    boss_spawn_sound = pygame.mixer.Sound('./assets/audio/boss-spawn.wav')

except pygame.error as e:
    print(f"Error loading sounds: {e}")
    main_menu_music = None 
    game_music = None
    boss_music = None

    button_hover_sound = None
    button_click_sound = None
    
    normal_hit_sound = None
    crit_hit_sound = None

    collect_xp_sound = None
    level_up_sound = None

    hurt_sound = None
    death_sound = None

    ability_obtained_sound = None
    ability_used_sound = None

    bat_death_sound = None
    boss_death_sound = None
    skeleton_death_sound = None
    blob_death_sound = None
    boss_spawn_sound = None

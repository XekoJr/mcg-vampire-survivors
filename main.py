import pygame
import sys
import os

pygame.init()  # Initialize Pygame

from settings import *
from player import Player
from enemy import spawn_enemy, draw_enemies, move_enemies, enemies
from projectile import draw_projectiles, move_projectiles, fire_projectile, projectiles
from xp import draw_xp_drops, xp_drops, xp_size
from utils import check_player_collisions, check_projectile_collisions

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Load and scale background image with error handling
try:
    menu_background = pygame.image.load("./images/background/gameart-cover.jpg")  # Replace with your file path
    menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))  # Scale to fit the screen
except pygame.error as e:
    print("Error loading menu background image:", e)
    menu_background = None  # Fallback to None if loading fails

# Load fonts
font_title = pygame.font.Font(pygame.font.match_font('arial'), 50)
font_button = pygame.font.Font(pygame.font.match_font('arial'), 30)
font_credit = pygame.font.Font(pygame.font.match_font('arial'), 20)
font_health = pygame.font.Font(pygame.font.match_font('arial'), 25)
font_score = pygame.font.Font(pygame.font.match_font('arial'), 25)

# Button setup
button_width, button_height = 200, 50
button_x = (WIDTH - button_width) // 2
button_y = HEIGHT // 2 -175  # Adjusted position for the "Start Game" button

def main_menu():
    player = Player()  # Create a new player instance
    reset_game(player)  # Reset game state

    running = True
    while running:
        # Draw the menu background if loaded
        if menu_background:
            screen.blit(menu_background, (0, 0))
        else:
            screen.fill(BLACK)  # Fallback to solid color if background fails to load

        # Draw Start button
        mouse_x, mouse_y = pygame.mouse.get_pos()
        button_color = DARK_RED if button_x < mouse_x < button_x + button_width and button_y < mouse_y < button_y + button_height else RED
        pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))
        button_text = font_button.render("Start Game", True, WHITE)
        screen.blit(button_text, (button_x + (button_width - button_text.get_width()) // 2, button_y + (button_height - button_text.get_height()) // 2))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_x < mouse_x < button_x + button_width and button_y < mouse_y < button_y + button_height:
                    running = False

        pygame.display.flip()

    game_loop(player)

def get_camera_offset(player):
    offset_x = max(0, min(player.x - WIDTH // 2, MAP_WIDTH - WIDTH))
    offset_y = max(0, min(player.y - HEIGHT // 2, MAP_HEIGHT - HEIGHT))
    return offset_x, offset_y

def game_over_screen(final_score):
    player = Player()  # Create a new player instance
    reset_game(player)  # Reset game state

    running = True
    while running:
        screen.fill(BLACK)

        # Display Game Over text
        game_over_text = font_title.render("Game Over", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4))

        # Display Final Score
        score_text = font_score.render(f"Final Score: {final_score}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 4 + 80))

        # Buttons for Restart and Main Menu
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Restart Button
        restart_button_color = DARK_RED if WIDTH // 2 - 100 < mouse_x < WIDTH // 2 + 100 and HEIGHT // 2 < mouse_y < HEIGHT // 2 + 50 else RED
        pygame.draw.rect(screen, restart_button_color, (WIDTH // 2 - 100, HEIGHT // 2, 200, 50))
        restart_text = font_button.render("Restart", True, WHITE)
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10))

        # Main Menu Button
        menu_button_color = DARK_RED if WIDTH // 2 - 100 < mouse_x < WIDTH // 2 + 100 and HEIGHT // 2 + 70 < mouse_y < HEIGHT // 2 + 120 else RED
        pygame.draw.rect(screen, menu_button_color, (WIDTH // 2 - 100, HEIGHT // 2 + 70, 200, 50))
        menu_text = font_button.render("Main Menu", True, WHITE)
        screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 2 + 80))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if WIDTH // 2 - 100 < mouse_x < WIDTH // 2 + 100 and HEIGHT // 2 < mouse_y < HEIGHT // 2 + 50:
                    game_loop(player)  # Restart the game
                if WIDTH // 2 - 100 < mouse_x < WIDTH // 2 + 100 and HEIGHT // 2 + 70 < mouse_y < HEIGHT // 2 + 120:
                    main_menu()  # Return to main menu

        pygame.display.flip()

def reset_game(player):
    """Resets all game state for a fresh start."""
    global enemies, xp_drops, projectiles  # Access global game objects
    enemies.clear()  # Clear all enemies
    xp_drops.clear()  # Clear all XP drops
    projectiles.clear()  # Clear all projectiles

    # Reset the player's state
    player.x = WIDTH // 2
    player.y = HEIGHT // 2
    player.health = 3
    player.xp = 0
    player.level = 1
    player.current_xp = 0
    player.xp_to_next_level = 50
    player.last_shot_time = 0
    player.score = 0
    player.fire_rate = fire_rate
    player.projectile_damage = 1
    player.level_up_pending = False

def level_up_menu(player):
    """Displays the level-up menu and lets the player choose an upgrade."""
    running = True
    while running:
        # Fill the screen with a solid background
        screen.fill(BLACK)

        # Draw the menu title
        title_text = font_title.render("Level Up!", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

        # Define the level-up options
        options = [
            {"text": "Increase Fire Rate by 20%", "upgrade": "fire_rate"},
            {"text": "Increase Damage by 20%", "upgrade": "damage"},
            {"text": "Restore 1 Health", "upgrade": "health"}
        ]

        # Render the options as buttons
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for i, option in enumerate(options):
            button_x = WIDTH // 2 - 150
            button_y = 200 + i * 100
            button_width = 300
            button_height = 50
            is_hovered = button_x < mouse_x < button_x + button_width and button_y < mouse_y < button_y + button_height
            button_color = DARK_RED if is_hovered else RED

            # Draw the button
            pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))
            option_text = font_button.render(option["text"], True, WHITE)
            screen.blit(option_text, (
                button_x + (button_width - option_text.get_width()) // 2,
                button_y + (button_height - option_text.get_height()) // 2
            ))

        # Process events for clicks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the click is inside any button
                for i, option in enumerate(options):
                    button_x = WIDTH // 2 - 150
                    button_y = 200 + i * 100
                    button_width = 300
                    button_height = 50
                    if button_x < mouse_x < button_x + button_width and button_y < mouse_y < button_y + button_height:
                        player.apply_upgrade(option["upgrade"])  # Apply the selected upgrade
                        running = False  # Exit the menu

        pygame.display.flip()

def game_loop(player):
    clock = pygame.time.Clock()
    frame_count = 0

    reset_game(player)  # Ensure game state is reset at the start of the loop

    running = True
    while running:
        screen.fill(GRAY)

        camera_x, camera_y = get_camera_offset(player)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        player.move()
        if pygame.time.get_ticks() - player.last_shot_time > player.fire_rate:
            fire_projectile(player, camera_x, camera_y)
            player.last_shot_time = pygame.time.get_ticks()

        frame_count += 1
        if frame_count >= enemy_spawn_rate:
            spawn_enemy()
            frame_count = 0

        move_projectiles()
        move_enemies(player.x, player.y)

        check_projectile_collisions(player)
        if check_player_collisions(player):
            player.health -= 1
            if player.health <= 0:
                game_over_screen(player.score)
                return  # Exit the game loop when the player dies

        if player.level_up_pending:
            level_up_menu(player)
            player.level_up_pending = False
            continue

        player.gain_xp(0)

        player.draw_with_offset(screen, camera_x, camera_y)
        draw_projectiles(screen, camera_x, camera_y)
        draw_enemies(screen, camera_x, camera_y)
        draw_xp_drops(screen, player, camera_x, camera_y)

        player.draw_health(screen)
        player.draw_score(screen)
        player.draw_xp(screen)

        pygame.display.flip()
        clock.tick(60)

main_menu()

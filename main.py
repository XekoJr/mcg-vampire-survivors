import random
import pygame
import sys
import os

pygame.init()

from settings import *
from player import Player
from enemy_manager import EnemyManager  # Import EnemyManager
from projectile import draw_projectiles, move_projectiles, fire_projectile, projectiles
from xp import draw_xp_drops, xp_drops
from utils import check_projectile_collisions, check_player_collisions

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Load and scale background image with error handling
try:
    menu_background = pygame.image.load("./assets/images/background/gameart-cover.jpg")
    menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))
except pygame.error as e:
    print("Error loading menu background image:", e)
    menu_background = None

# Load fonts
font_title = pygame.font.Font(pygame.font.match_font('arial'), 50)
font_button = pygame.font.Font(pygame.font.match_font('arial'), 30)
font_credit = pygame.font.Font(pygame.font.match_font('arial'), 20)
font_health = pygame.font.Font(pygame.font.match_font('arial'), 25)
font_score = pygame.font.Font(pygame.font.match_font('arial'), 25)

button_width, button_height = 200, 50
button_x = (WIDTH - button_width) // 2
button_y = HEIGHT // 2 - 175

def main_menu():
    player = Player()
    enemy_manager = EnemyManager()  # Initialize EnemyManager
    reset_game(enemy_manager)

    running = True
    while running:
        if menu_background:
            screen.blit(menu_background, (0, 0))
        else:
            screen.fill(BLACK)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        button_color = DARK_RED if button_x < mouse_x < button_x + button_width and button_y < mouse_y < button_y + button_height else RED
        pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))
        button_text = font_button.render("Start Game", True, WHITE)
        screen.blit(button_text, (button_x + (button_width - button_text.get_width()) // 2, button_y + (button_height - button_text.get_height()) // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_x < mouse_x < button_x + button_width and button_y < mouse_y < button_y + button_height:
                    running = False

        pygame.display.flip()

    game_loop(player, enemy_manager)

def game_over_screen(final_score, enemy_manager):
    """Display the Game Over screen."""
    player = Player()  # Create a new player instance
    reset_game(enemy_manager)  # Reset the game state

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

        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Restart Button
                if WIDTH // 2 - 100 < mouse_x < WIDTH // 2 + 100 and HEIGHT // 2 < mouse_y < HEIGHT // 2 + 50:
                    game_loop(player, enemy_manager)  # Restart the game
                    return
                # Main Menu Button
                if WIDTH // 2 - 100 < mouse_x < WIDTH // 2 + 100 and HEIGHT // 2 + 70 < mouse_y < HEIGHT // 2 + 120:
                    main_menu()  # Return to main menu
                    return

        pygame.display.flip()


def reset_game(enemy_manager):
    global projectiles, xp_drops
    projectiles.clear()
    xp_drops.clear()
    enemy_manager.enemies.clear()

    player = Player()

def get_camera_offset(player):
    offset_x = max(0, min(player.x - WIDTH // 2, MAP_WIDTH - WIDTH))
    offset_y = max(0, min(player.y - HEIGHT // 2, MAP_HEIGHT - HEIGHT))
    return offset_x, offset_y

def level_up_menu(player):
    """Displays the level-up menu and lets the player choose an upgrade."""
    running = True

    # Define all possible upgrades
    all_upgrades = [
        {"text": "Increase Fire Rate by 20%", "upgrade": "fire_rate"},
        {"text": "Increase Damage by 30%", "upgrade": "damage"},
        {"text": "Restore 50 HP", "upgrade": "health"},
        {"text": "Increase Max Health by 25", "upgrade": "max_health"},
        {"text": "Increase Speed by 13%", "upgrade": "speed"},
        {"text": "Increase Crit Chance by 5%", "upgrade": "crit_chance"}
    ]

    # Randomly select 3 upgrades
    selected_upgrades = random.sample(all_upgrades, 3)

    while running:
        screen.fill(BLACK)
        title_text = font_title.render("Level Up!", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        for i, option in enumerate(selected_upgrades):
            button_x = WIDTH // 2 - 175
            button_y = 200 + i * 100
            button_width = 350
            button_height = 50
            is_hovered = button_x < mouse_x < button_x + button_width and button_y < mouse_y < button_y + button_height
            button_color = DARK_RED if is_hovered else RED

            pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))
            option_text = font_button.render(option["text"], True, WHITE)
            screen.blit(option_text, (
                button_x + (button_width - option_text.get_width()) // 2,
                button_y + (button_height - option_text.get_height()) // 2
            ))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, option in enumerate(selected_upgrades):
                    button_x = WIDTH // 2 - 150
                    button_y = 200 + i * 100
                    if button_x < mouse_x < button_x + button_width and button_y < mouse_y < button_y + button_height:
                        player.apply_upgrade(option["upgrade"])
                        running = False

        pygame.display.flip()

    # Update last_shot_time to avoid firing immediately after exiting
    player.last_shot_time = pygame.time.get_ticks()

def game_loop(player, enemy_manager):
    clock = pygame.time.Clock()
    frame_count = 0
    reset_game(enemy_manager)

    running = True
    while running:
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
        if frame_count >= enemy_manager.spawn_interval:
            enemy_manager.spawn_enemy(player.level)
            frame_count = 0


        move_projectiles()
        enemy_manager.update_enemies(player.x, player.y)

        enemy_manager.handle_projectile_collisions(projectiles, player, xp_drops)
        if enemy_manager.handle_player_collisions(player):
            player.health -= 25
            if player.health <= 0:
                game_over_screen(player.score, enemy_manager)
                return

        if player.level_up_pending:
            level_up_menu(player)
            player.level_up_pending = False
            continue

        player.gain_xp(0)

        screen.fill(GRAY)
        player.draw_with_offset(screen, camera_x, camera_y)
        draw_projectiles(screen, camera_x, camera_y)
        enemy_manager.draw_enemies(screen, camera_x, camera_y)
        draw_xp_drops(screen, player, camera_x, camera_y)

        player.draw_health(screen)
        player.draw_score(screen)
        player.draw_xp(screen)

        pygame.display.flip()
        clock.tick(60)

main_menu()

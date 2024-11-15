import pygame
import sys
import os

pygame.init()  # Initialize Pygame

from settings import *
from player import Player
from enemy import spawn_enemy, draw_enemies, move_enemies, enemies
from projectile import draw_projectiles, move_projectiles, fire_projectile, projectiles
from xp import draw_xp_drops, xp_drops
from utils import check_player_collisions, check_projectile_collisions

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vampyre Survivors Game")

# Check if background image exists
print("Background image exists:", os.path.exists("grass_background.png"))

# Load and scale background image with error handling
try:
    background = pygame.image.load("grass_background.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Scale to fit the screen
except pygame.error as e:
    print("Error loading background image:", e)
    background = None  # Fallback to None if loading fails


# Load fonts (only in main.py)
font_title = pygame.font.Font(pygame.font.match_font('arial'), 50)
font_button = pygame.font.Font(pygame.font.match_font('arial'), 30)
font_credit = pygame.font.Font(pygame.font.match_font('arial'), 20)
font_health = pygame.font.Font(pygame.font.match_font('arial'), 25)
font_score = pygame.font.Font(pygame.font.match_font('arial'), 25)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vampyre Survivors Game")

def main_menu():
    running = True
    while running:
        screen.fill(BLACK)
        # Draw title and credits
        title_text = font_title.render("Vampyre Survivors", True, WHITE)
        credit_text = font_credit.render("Created by Peter Spore PS Copenhagen Origami Bags", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))
        screen.blit(credit_text, (WIDTH // 2 - credit_text.get_width() // 2, HEIGHT - 50))

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

    game_loop()
    
def game_over_screen(final_score):
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

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if Restart button is clicked
                if WIDTH // 2 - 100 < mouse_x < WIDTH // 2 + 100 and HEIGHT // 2 < mouse_y < HEIGHT // 2 + 50:
                    game_loop()  # Restart the game
                # Check if Main Menu button is clicked
                if WIDTH // 2 - 100 < mouse_x < WIDTH // 2 + 100 and HEIGHT // 2 + 70 < mouse_y < HEIGHT // 2 + 120:
                    main_menu()  # Return to main menu

        pygame.display.flip()


def game_loop():
    clock = pygame.time.Clock()
    player = Player()
    frame_count = 0

    running = True
    while running:
        # Draw the background image if loaded successfully
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(GRAY) 

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update player, enemies, projectiles, and other game elements
        player.move()
        if pygame.time.get_ticks() - player.last_shot_time > fire_rate:
            fire_projectile(player)
            player.last_shot_time = pygame.time.get_ticks()

        # Spawn enemies
        frame_count += 1
        if frame_count >= enemy_spawn_rate:
            spawn_enemy()
            frame_count = 0

        # Move projectiles and enemies
        move_projectiles()
        move_enemies(player.x, player.y)

        # Check for collisions
        check_projectile_collisions(player)
        if check_player_collisions(player):
            player.health -= 1
            if player.health <= 0:
                game_over_screen(player.score)  # Show game over screen with the final score
                return  # Exit the game loop after game over screen

        # Draw game elements
        player.draw(screen)
        player.draw_health(screen)
        player.draw_score(screen)
        player.draw_xp(screen)
        draw_projectiles(screen)
        draw_enemies(screen)
        draw_xp_drops(screen, player)

        pygame.display.flip()
        clock.tick(60)

# Run the menu
main_menu()

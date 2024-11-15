import pygame
import sys
from settings import *
from player import Player
from enemy import spawn_enemy, draw_enemies, move_enemies, enemies
from projectile import draw_projectiles, move_projectiles, fire_projectile, projectiles
from xp import draw_xp_drops, xp_drops
from utils import check_player_collisions, check_projectile_collisions

# Initialize Pygame
pygame.init()
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

def game_loop():
    clock = pygame.time.Clock()
    player = Player()
    frame_count = 0

    running = True
    while running:
        screen.fill(GRAY)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        player.move()
        if pygame.time.get_ticks() - player.last_shot_time > fire_rate:
            fire_projectile(player)
            player.last_shot_time = pygame.time.get_ticks()

        # Spawn enemies
        frame_count += 1
        if frame_count >= enemy_spawn_rate:
            spawn_enemy()
            frame_count = 0

        # Update and draw entities
        move_projectiles()
        move_enemies(player.x, player.y)
        check_projectile_collisions(player)
        if check_player_collisions(player):
            player.health -= 1
            if player.health <= 0:
                print("Game Over")
                running = False

        player.draw(screen)
        draw_projectiles(screen)
        draw_enemies(screen)
        draw_xp_drops(screen, player)
        player.draw_score(screen)
        player.draw_xp(screen)

        pygame.display.flip()
        clock.tick(60)

# Run the menu
main_menu()

import pygame

pygame.init()
pygame.mixer.init()

import random
import sys
from settings import *
from player import Player
from enemy_manager import EnemyManager
from enemies.boss_1_enemy import Boss1Enemy
from projectile import *
from xp import draw_xp_drops, xp_drops
from menu import Menu

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Initialize the menu
menu = Menu(screen)

def reset_game(enemy_manager):
    global projectiles, xp_drops
    projectiles.clear()
    xp_drops.clear()
    enemy_manager.enemies.clear()
    return Player()  # Return a new player instance

def get_camera_offset(player):
    offset_x = max(0, min(player.x - WIDTH // 2, MAP_WIDTH - WIDTH))
    offset_y = max(0, min(player.y - HEIGHT // 2, MAP_HEIGHT - HEIGHT))
    return offset_x, offset_y

def game_loop(player, enemy_manager):
    clock = pygame.time.Clock()
    boss_projectiles.clear()
    frame_count = 0

    reset_game(enemy_manager)

    running = True
    main_menu_music.stop()
    game_music.play(-1)

    while running:
        camera_x, camera_y = get_camera_offset(player)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Player movement and shooting
        player.move()
        if pygame.time.get_ticks() - player.last_shot_time > player.fire_rate:
            fire_projectile(player, camera_x, camera_y)
            player.last_shot_time = pygame.time.get_ticks()

        # Spawn enemies and boss behavior
        frame_count += 1
        if frame_count >= enemy_manager.spawn_interval:
            enemy_manager.spawn_enemy(player.level)
            frame_count = 0

        enemy_manager.update_enemies(player.x, player.y, player, screen, camera_x, camera_y)
        
        move_projectiles()
        move_boss_projectiles()

        # Handle boss shooting
        for enemy in enemy_manager.enemies:
            if isinstance(enemy, Boss1Enemy):
                enemy.shoot_at_player(player)

        # Handle collisions
        enemy_manager.handle_projectile_collisions(projectiles, player, xp_drops)
        if enemy_manager.handle_player_collisions(player):
            if player.health <= 0:
                new_player = menu.game_over_screen(player.score, enemy_manager, reset_game, game_loop)
                if new_player:
                    game_loop(new_player, enemy_manager)
                return

        # Draw everything
        screen.fill(GRAY)
        player.draw_with_offset(screen, camera_x, camera_y)
        draw_projectiles(screen, camera_x, camera_y)
        draw_boss_projectiles(screen, camera_x, camera_y)
        enemy_manager.draw_enemies(screen, camera_x, camera_y, player)
        draw_xp_drops(screen, player, camera_x, camera_y)

        if player.level_up_pending:
            menu.level_up_menu(player, screen)
            player.level_up_pending = False
            continue

        player.draw_health(screen)
        player.draw_score(screen)
        player.draw_xp(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    player = Player()
    enemy_manager = EnemyManager()
    menu.main_menu(player, enemy_manager, reset_game, game_loop)
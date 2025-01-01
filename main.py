import pygame

pygame.init()
pygame.mixer.init()

import random
import sys
from settings import *
from player import Player
from enemy_manager import EnemyManager
from enemies.__init__ import *
from abilities.__init__ import *
from projectile import *
from xp import draw_xp_drops, xp_drops
from menu import Menu

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Initialize the menu
menu = Menu(screen)

# Globals for the current player and enemy manager
current_player = None
current_enemy_manager = None

def reset_game(achievements=None):
    """Reset the game state, including the player, enemies, projectiles, and abilities."""
    global current_player, current_enemy_manager
    projectiles.clear()
    xp_drops.clear()

    settings = menu.load_settings()
    if achievements is None:
        achievements = settings.get("achievements", {})  # Use provided achievements if available

    # Reinitialize the player and enemy manager
    current_player = Player()
    skills = settings.get("skills", {})
    current_player.initialize_abilities(skills)
    current_player.apply_skill_upgrades(skills)
    current_player.apply_stat_upgrades(skills)

    current_enemy_manager = EnemyManager()
    current_enemy_manager.enemies.clear()

    return current_player, current_enemy_manager, achievements

def get_camera_offset(player):
    screen_width = pygame.display.get_surface().get_width()
    screen_height = pygame.display.get_surface().get_height()

    offset_x = max(0, min(player.x - screen_width // 2, MAP_WIDTH - screen_width))
    offset_y = max(0, min(player.y - screen_height // 2, MAP_HEIGHT - screen_height))

    return offset_x, offset_y

def game_loop(player, enemy_manager, achievements):
    clock = pygame.time.Clock()
    boss_projectiles.clear()
    frame_count = 0

    # Music management
    main_menu_music.stop()
    game_music.play(-1)

    running = True

    while running:
        camera_x, camera_y = get_camera_offset(player)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # Pause the game and display the pause menu
                return_to_menu = menu.pause_menu(reset_game=reset_game, game_loop=game_loop, achievements=achievements)
                if return_to_menu:
                    # Return to the main menu
                    return

        # Player movement and shooting
        player.move()
        if pygame.time.get_ticks() - player.last_shot_time > player.fire_rate:
            fire_projectile(player, camera_x, camera_y)
            player.last_shot_time = pygame.time.get_ticks()

        # Spawn enemies and boss behaviors
        frame_count += 1
        if frame_count >= enemy_manager.spawn_interval:
            enemy_manager.spawn_enemy(player.level)
            frame_count = 0

        enemy_manager.update_enemies(player.x, player.y, player, screen, camera_x, camera_y)

        move_projectiles()
        move_boss_projectiles()

        # Handle enemy interactionsa
        for enemy in enemy_manager.enemies:
            # Apply active abilities
            for ability in player.abilities:
                if ability.active:
                    if isinstance(ability, ShieldAbility):
                        ability.update() 
                    elif isinstance(ability, BurningAbility):
                        ability.update_burn(enemy)
                    elif isinstance(ability, HealingAbility):
                        ability.heal(player)
                    elif isinstance(ability, InvincibilityAbility):
                        ability.apply_invincibility(player)

            # Boss-specific behavior
            if isinstance(enemy, Boss1Enemy):
                enemy.shoot_at_player(player)

        # Projectile and player collision handling
        for projectile in boss_projectiles[:]:
            projectile['x'] += projectile['dx'] * projectile['speed']
            projectile['y'] += projectile['dy'] * projectile['speed']

            projectile_rect = pygame.Rect(
                projectile['x'], 
                projectile['y'], 
                boss_projectile_frames[0].get_width(),
                boss_projectile_frames[0].get_height()
            )
            player_rect = pygame.Rect(player.x, player.y, player.size, player.size)

            # Check for collision with the player by boss projectiles
            if player_rect.colliderect(projectile_rect):
                # Check for active ShieldAbility
                for ability in player.abilities:
                    if isinstance(ability, ShieldAbility) and ability.block(player):
                        block_hit_sound.play()
                        boss_projectiles.remove(projectile)  # Remove the projectile since it was blocked
                        break  # Exit the loop over `boss_projectiles` since the shield blocked the projectile
                else:  # Shield didn't block, proceed with damage logic
                    # Check for invincibility
                    current_time = pygame.time.get_ticks()
                    if current_time - player.last_damage_time < player.invincibility_time * 1000:
                        boss_projectiles.remove(projectile)  # Remove the projectile without applying damage
                        continue  # Skip further damage logic

                    # Apply damage to the player
                    player.health -= projectile['damage']
                    player.last_damage_time = current_time  # Update the last damage time for invincibility
                    hurt_sound.play()

                    player.apply_status(
                        "burn", 
                        3, 
                        0.5, 
                        5, 
                        "Boss"
                    )  # Apply burn status to the player

                    # Check if the player's health has reached 0 or below
                    if player.health <= 0:
                        death_sound.play()
                        new_player, new_enemy_manager, achievements = reset_game(achievements=achievements)
                        menu.game_over_screen(player.score, new_enemy_manager, reset_game, game_loop, achievements)
                        return  # Exit the game loop

                # Remove the projectile
                if projectile in boss_projectiles:
                    boss_projectiles.remove(projectile)

            # Remove the projectile if it goes out of bounds
            if (projectile['x'] < 0 or projectile['x'] > MAP_WIDTH or
                    projectile['y'] < 0 or projectile['y'] > MAP_HEIGHT):
                if projectile in boss_projectiles:
                    boss_projectiles.remove(projectile)

        # Handle collisions
        enemy_manager.handle_projectile_collisions(projectiles, player, xp_drops, achievements, menu.save_settings)
        for enemy in enemy_manager.enemies[:]:
            if enemy.is_dead():
                achievements = enemy_manager.handle_enemy_defeat(enemy, player, xp_drops, achievements, menu.save_settings)

        # Handle player collisions with enemies
        if enemy_manager.handle_player_collisions(player):
            # Check if the player is dead
            if player.health <= 0:
                death_sound.play()
                new_player, new_enemy_manager, achievements = reset_game()
                menu.game_over_screen(player.score, new_enemy_manager, reset_game, game_loop, achievements)
                return

        # Calculate background position
        background_x = -camera_x
        background_y = -camera_y

        # Draw the background
        screen.blit(background_image, (background_x, background_y))

        # Draw game elements
        player.draw_with_offset(screen, camera_x, camera_y)
        draw_projectiles(screen, camera_x, camera_y)
        enemy_manager.draw_enemies(screen, camera_x, camera_y, player)
        draw_boss_projectiles(screen, camera_x, camera_y)
        draw_xp_drops(screen, player, camera_x, camera_y)

        if player.level_up_pending:
            menu.level_up_menu(player, screen)
            player.level_up_pending = False
            continue

        player.draw_health(screen)
        player.draw_score(screen)
        player.draw_xp(screen)

        # Status and ability iconsd
        player.update_status_effects()
        if player.health <= 0:
            death_sound.play()
            new_player, new_enemy_manager, achievements = reset_game()
            menu.game_over_screen(player.score, new_enemy_manager, reset_game, game_loop, achievements)
            return
        player.update_abilities_effects()
        player.draw_status_abilities_icons(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    current_player, current_enemy_manager, achievements = reset_game()
    menu.main_menu(current_player, current_enemy_manager, reset_game, game_loop, achievements)

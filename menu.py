import json
import pygame
import sys
import random
from player import Player
from settings import *

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.menu_background = self.load_menu_background()
        self.settings_file = "./utils.json"
        self.volume_settings = self.load_volume_settings()
        self.high_score = self.load_high_score()

    def load_menu_background(self):
        try:
            menu_background = pygame.image.load("./assets/images/background/gameart-cover.jpg")
            return pygame.transform.scale(menu_background, (WIDTH, HEIGHT))
        except pygame.error as e:
            print("Error loading menu background image:", e)
            return None

    def load_volume_settings(self):
        """Load the volume settings from the utils.json file, or create defaults if the file is empty or missing."""
        default_settings = {
            "master_volume": 100,
            "music_volume": 100,
            "effects_volume": 100,
            "high_score": 0,
        }
        try:
            with open(self.settings_file, "r") as f:
                settings = json.load(f)
                # Ensure all default keys are present
                for key, value in default_settings.items():
                    if key not in settings:
                        settings[key] = value
        except (FileNotFoundError, json.JSONDecodeError):
            settings = default_settings  # Use default settings if file is missing or corrupted
            with open(self.settings_file, "w") as f:
                json.dump(settings, f, indent=4)
        return settings

    def save_volume_settings(self):
        """Save the volume settings to the utils.json file."""
        try:
            with open(self.settings_file, "r+") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {}
                # Update or initialize keys
                data["master_volume"] = self.volume_settings["master_volume"]
                data["music_volume"] = self.volume_settings["music_volume"]
                data["effects_volume"] = self.volume_settings["effects_volume"]
                data["high_score"] = max(data.get("high_score", 0), self.high_score)  # Keep the highest score
                # Write back to the file
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
        except FileNotFoundError:
            with open(self.settings_file, "w") as f:
                json.dump(self.volume_settings, f, indent=4)

    def load_high_score(self):
        try:
            with open(self.settings_file, "r") as f:
                data = json.load(f)
                return data.get("high_score", 0)
        except FileNotFoundError:
            return 0
        
    def save_high_score(self, score):
        try:
            with open(self.settings_file, "r+") as f:
                data = json.load(f)
                data["high_score"] = score
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
        except FileNotFoundError:
            with open(self.settings_file, "w") as f:
                json.dump({"high_score": score}, f, indent=4)

    def main_menu(self, player, enemy_manager, reset_game, game_loop):
        """Displays the main menu."""
        running = True

        main_menu_music.play(-1)  # Loop the music indefinitely

        while running:
            if self.menu_background:
                self.screen.blit(self.menu_background, (0, 0))
            else:
                self.screen.fill(BLACK)

            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Display high score
            if self.high_score > 0:
                high_score_text = font_score.render(f"High Score: {self.high_score}", True, WHITE)
                self.screen.blit(high_score_text, (WIDTH - high_score_text.get_width() - 20, 20))

            # Start Game Button
            button_color = DARK_RED if button_x < mouse_x < button_x + button_width and \
                                       button_y < mouse_y < button_y + button_height else RED
            pygame.draw.rect(self.screen, button_color, (button_x, button_y, button_width, button_height))
            button_text = font_button.render("Start Game", True, WHITE)
            self.screen.blit(button_text, (button_x + (button_width - button_text.get_width()) // 2,
                                           button_y + (button_height - button_text.get_height()) // 2))

            # Settings Button
            settings_y = button_y + 70 
            settings_button_color = DARK_RED if button_x < mouse_x < button_x + button_width and \
                                                  settings_y < mouse_y < settings_y + button_height else RED
            pygame.draw.rect(self.screen, settings_button_color, (button_x, settings_y, button_width, button_height))
            settings_text = font_button.render("Settings", True, WHITE)
            self.screen.blit(settings_text, (button_x + (button_width - settings_text.get_width()) // 2,
                                             settings_y + (button_height - settings_text.get_height()) // 2))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_x < mouse_x < button_x + button_width and button_y < mouse_y < button_y + button_height:
                        running = False
                    if button_x < mouse_x < button_x + button_width and settings_y < mouse_y < settings_y + button_height:
                        self.settings_menu()

            pygame.display.flip()

        reset_game(enemy_manager)
        game_loop(player, enemy_manager)

    def settings_menu(self):
        """Displays the settings menu."""
        running = True

        while running:
            self.screen.fill(BLACK)

            # Render the title text
            title_text = font_title.render("Settings", True, WHITE)
            self.screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

            # Define settings options
            options = [
                {"label": "Master Volume", "key": "master_volume"},
                {"label": "Music Volume", "key": "music_volume"},
                {"label": "Effects Volume", "key": "effects_volume"}
            ]

            mouse_x, mouse_y = pygame.mouse.get_pos()

            for i, option in enumerate(options):
                # Sliders and labels
                label = font_button.render(f"{option['label']}: {self.volume_settings.get(option['key'], 100)}%", True, WHITE)
                slider_x = WIDTH // 2 - 150
                slider_y = 150 + i * 100
                slider_width = 300
                slider_height = 20

                pygame.draw.rect(self.screen, GRAY, (slider_x, slider_y, slider_width, slider_height))
                slider_fill_width = int((self.volume_settings[option['key']] / 100) * slider_width)
                pygame.draw.rect(self.screen, GREEN, (slider_x, slider_y, slider_fill_width, slider_height))
                self.screen.blit(label, (slider_x, slider_y - 40))

                # Handle slider interaction
                if pygame.mouse.get_pressed()[0] and slider_x <= mouse_x <= slider_x + slider_width and \
                        slider_y <= mouse_y <= slider_y + slider_height:
                    new_value = int(((mouse_x - slider_x) / slider_width) * 100)
                    self.volume_settings[option['key']] = max(0, min(100, new_value))

                    # Apply volume changes dynamically
                    master_volume = self.volume_settings["master_volume"] / 100
                    if option['key'] == "master_volume":
                        # Update master volume and recalculate dependent volumes
                        pygame.mixer.music.set_volume(master_volume)  # Apply master volume to global music
                        # Reapply music and effects volumes with master volume factored in
                        music_volume = self.volume_settings["music_volume"] / 100 * master_volume
                        for music in [main_menu_music, game_music]:
                            if music:
                                music.set_volume(music_volume)

                        effects_volume = self.volume_settings["effects_volume"] / 100 * master_volume
                        for sound in [normal_hit_sound, crit_hit_sound, collect_xp_sound, level_up_sound]:
                            if sound:
                                sound.set_volume(effects_volume)
                    elif option['key'] == "music_volume":
                        # Apply music volume adjusted by master volume
                        music_volume = self.volume_settings["music_volume"] / 100 * master_volume
                        for music in [main_menu_music, game_music]:
                            if music:
                                music.set_volume(music_volume)
                    elif option['key'] == "effects_volume":
                        # Apply effects volume adjusted by master volume
                        effects_volume = self.volume_settings["effects_volume"] / 100 * master_volume
                        for sound in [normal_hit_sound, crit_hit_sound, collect_xp_sound, level_up_sound]:
                            if sound:
                                sound.set_volume(effects_volume)

            # Back Button
            back_button_x = WIDTH // 2 - 100
            back_button_y = 450
            back_button_color = DARK_RED if back_button_x < mouse_x < back_button_x + 200 and \
                                           back_button_y < mouse_y < back_button_y + 50 else RED
            pygame.draw.rect(self.screen, back_button_color, (back_button_x, back_button_y, 200, 50))
            back_text = font_button.render("Back", True, WHITE)
            self.screen.blit(back_text, (
                back_button_x + (200 - back_text.get_width()) // 2,
                back_button_y + (50 - back_text.get_height()) // 2
            ))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button_x < mouse_x < back_button_x + 200 and back_button_y < mouse_y < back_button_y + 50:
                        self.save_volume_settings()
                        running = False

            pygame.display.flip()

    def game_over_screen(self, score, enemy_manager, reset_game, game_loop):
        """Display the Game Over screen."""
        
        game_music.stop()
        
        running = True

        # Update high score if necessary
        if score > self.high_score:
            self.high_score = score
            self.save_high_score(score)

        while running:
            self.screen.fill(BLACK)

            # Display "Game Over" text
            game_over_text = font_title.render("Game Over", True, WHITE)
            self.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4))

            # Display Final Score
            score_text = font_score.render(f"Final Score: {score}", True, WHITE)
            self.screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 4 + 80))

            # Buttons for Restart and Return to Menu
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Restart Button
            restart_button_color = DARK_RED if WIDTH // 2 - 100 < mouse_x < WIDTH // 2 + 100 and HEIGHT // 2 < mouse_y < HEIGHT // 2 + 50 else RED
            pygame.draw.rect(self.screen, restart_button_color, (WIDTH // 2 - 100, HEIGHT // 2, 200, 50))
            restart_text = font_button.render("Restart", True, WHITE)
            self.screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10))

            # Main Menu Button
            menu_button_color = DARK_RED if WIDTH // 2 - 100 < mouse_x < WIDTH // 2 + 100 and HEIGHT // 2 + 70 < mouse_y < HEIGHT // 2 + 120 else RED
            pygame.draw.rect(self.screen, menu_button_color, (WIDTH // 2 - 100, HEIGHT // 2 + 70, 200, 50))
            menu_text = font_button.render("Main Menu", True, WHITE)
            self.screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 2 + 80))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Restart Button
                    if WIDTH // 2 - 100 < mouse_x < WIDTH // 2 + 100 and HEIGHT // 2 < mouse_y < HEIGHT // 2 + 50:
                        new_player = Player()  # Create a new player instance
                        reset_game(enemy_manager)  # Reset the game state
                        running = False
                        game_loop(new_player, enemy_manager)
                        return
                    # Main Menu Button
                    if WIDTH // 2 - 100 < mouse_x < WIDTH // 2 + 100 and HEIGHT // 2 + 70 < mouse_y < HEIGHT // 2 + 120:
                        new_player = Player()  # Create a new player instance
                        reset_game(enemy_manager)  # Reset the game state
                        running = False
                        self.main_menu(new_player, enemy_manager, reset_game, game_loop)
                        return

            pygame.display.flip()

    def level_up_menu(self, player, screen):
        """Displays the level-up menu and lets the player choose an upgrade."""
        running = True

        # Play the level-up sound
        try:
            level_up_sound.play()
        except NameError:
            print("Level-up sound not initialized.")

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
            self.screen.fill(BLACK)  # Use the correct screen object

            # Render the title text
            title_text = font_title.render("Level Up!", True, WHITE)
            screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

            # Mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Draw buttons and check hover
            button_rects = []  # Store button rects for later click detection
            for i, option in enumerate(selected_upgrades):
                # Button dimensions
                button_x = WIDTH // 2 - 175
                button_y = 200 + i * 100
                button_width = 350
                button_height = 50

                # Detect hover
                is_hovered = button_x < mouse_x < button_x + button_width and button_y < mouse_y < button_y + button_height
                button_color = DARK_RED if is_hovered else RED

                # Draw the button
                pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))

                # Render button text
                option_text = font_button.render(option["text"], True, WHITE)
                screen.blit(option_text, (
                    button_x + (button_width - option_text.get_width()) // 2,
                    button_y + (button_height - option_text.get_height()) // 2
                ))

                # Add button rect for click detection
                button_rects.append(pygame.Rect(button_x, button_y, button_width, button_height))

            # Handle events outside of button loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, rect in enumerate(button_rects):
                        if rect.collidepoint(mouse_x, mouse_y):  # Check if click is inside button rect
                            player.apply_upgrade(selected_upgrades[i]["upgrade"])
                            running = False  # Exit menu

            pygame.display.flip()

        # Update last_shot_time to avoid firing immediately after exiting the menu
        player.last_shot_time = pygame.time.get_ticks()


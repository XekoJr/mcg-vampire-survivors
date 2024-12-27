import json
import pygame
import sys
import random
from player import Player
from settings import *

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.settings_file = "./utils.json"
        self.settings = self.load_settings()
        self.menu_background = self.load_menu_background()
        self.high_score = self.load_high_score()
        self.resolutions = [
            (1366, 768), (1280, 720), (1024, 576)
        ]

    def load_menu_background(self):
        """Load and scale the menu background to the current resolution."""
        try:
            # Load the background image
            menu_background = pygame.image.load("./assets/images/background/gameart-cover.jpg")
            
            # Dynamically stretch the background to fit the resolution
            scaled_background = pygame.transform.scale(menu_background, (self.screen.get_width(), self.screen.get_height()))
            return scaled_background
        except pygame.error as e:
            print("Error loading menu background image:", e)
            return None

    def load_settings(self):
        """Load the settings from the utils.json file, or create defaults if the file is empty or missing."""
        default_settings = {
            "master_volume": 100,
            "music_volume": 100,
            "effects_volume": 100,
            "resolution": (1280, 720),
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

        # Apply resolution on load
        pygame.display.set_mode(settings["resolution"])

        # Define default volumes for all sounds
        default_volumes = {
            "main_menu_music": 0.05,
            "game_music": 0.1,
            "boss_music": 0.1,
            "hover_sound": 0.3,
            "click_sound": 0.3,
            "normal_hit_sound": 0.5,
            "crit_hit_sound": 0.6,
            "collect_xp_sound": 0.5,
            "level_up_sound": 0.5,
            "hurt_sound": 0.5,
            "death_sound": 1.0,
            "ability_obtained_sound": 0.5,
            "ability_used_sound": 0.5,
            "bat_death_sound": 0.05,
            "boss_death_sound": 0.5,
            "skeleton_death_sound": 0.6,
            "blob_death_sound": 1.3,
            "boss_spawn_sound": 0.5,
        }

        # Minimum volume threshold
        min_volume = 0.01  # 1% volume minimum

        # Apply volume settings
        master_volume = max(settings["master_volume"] / 100, min_volume)
        music_volume = max((settings["music_volume"] / 100) * master_volume, min_volume)
        effects_volume = max((settings["effects_volume"] / 100) * master_volume, min_volume)

        # Scale and apply volumes for music
        if main_menu_music: main_menu_music.set_volume(max(default_volumes["main_menu_music"] * music_volume, min_volume))
        if game_music: game_music.set_volume(max(default_volumes["game_music"] * music_volume, min_volume))
        if boss_music: boss_music.set_volume(max(default_volumes["boss_music"] * music_volume, min_volume))

        # Scale and apply volumes for effects
        for sound_key, sound_obj in {
            "hover_sound": hover_sound,
            "click_sound": click_sound,
            "normal_hit_sound": normal_hit_sound,
            "crit_hit_sound": crit_hit_sound,
            "collect_xp_sound": collect_xp_sound,
            "level_up_sound": level_up_sound,
            "hurt_sound": hurt_sound,
            "death_sound": death_sound,
            "ability_obtained_sound": ability_obtained_sound,
            "ability_used_sound": ability_used_sound,
            "bat_death_sound": bat_death_sound,
            "boss_death_sound": boss_death_sound,
            "skeleton_death_sound": skeleton_death_sound,
            "blob_death_sound": blob_death_sound,
            "boss_spawn_sound": boss_spawn_sound,
        }.items():
            if sound_obj:
                sound_obj.set_volume(max(default_volumes[sound_key] * effects_volume, min_volume))

        return settings

    def save_settings(self):
        """Save the settings to the utils.json file."""
        try:
            with open(self.settings_file, "r+") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {}
                # Update or initialize keys
                data.update(self.settings)
                data["resolution"] = self.settings.get("resolution", (1366, 768))
                data["high_score"] = max(data.get("high_score", 0), self.high_score)  # Keep the highest score
                # Write back to the file
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
        except FileNotFoundError:
            with open(self.settings_file, "w") as f:
                json.dump(self.settings, f, indent=4)

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
        hover_sound.set_volume(0.5)  # Adjust volume if necessary
        click_sound.set_volume(0.5)

        main_menu_music.play(-1)  # Loop the music indefinitely

        running = True
        button_margin = 20  # Margin between buttons and screen edges
        button_width, button_height = 200, 50

        # To track hover state and play sound only once per hover
        hovered_button = None

        while running:
            if self.menu_background:
                self.screen.blit(self.menu_background, (0, 0))
            else:
                self.screen.fill(BLACK)

            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Display high score in the top-right corner
            if self.high_score > 0:
                high_score_text = font_score.render(f"High Score: {self.high_score}", True, WHITE)
                self.screen.blit(high_score_text, (
                    self.screen.get_width() - high_score_text.get_width() - button_margin,
                    button_margin
                ))

            # Define button positions (bottom-left alignment)
            button_x = button_margin
            button_y = self.screen.get_height() - (button_height * 2) - button_margin * 3

            # Start Game Button
            start_hovered = button_x < mouse_x < button_x + button_width and \
                            button_y < mouse_y < button_y + button_height
            button_color = DARK_RED if start_hovered else RED
            pygame.draw.rect(self.screen, button_color, (button_x, button_y, button_width, button_height))
            button_text = font_button.render("Start Game", True, WHITE)
            self.screen.blit(button_text, (
                button_x + (button_width - button_text.get_width()) // 2,
                button_y + (button_height - button_text.get_height()) // 2
            ))

            # Settings Button
            settings_y = button_y + button_height + button_margin
            settings_hovered = button_x < mouse_x < button_x + button_width and \
                            settings_y < mouse_y < settings_y + button_height
            settings_button_color = DARK_RED if settings_hovered else RED
            pygame.draw.rect(self.screen, settings_button_color, (button_x, settings_y, button_width, button_height))
            settings_text = font_button.render("Settings", True, WHITE)
            self.screen.blit(settings_text, (
                button_x + (button_width - settings_text.get_width()) // 2,
                settings_y + (button_height - settings_text.get_height()) // 2
            ))

            # Play hover sound when hovering over a button
            if start_hovered and hovered_button != "start":
                hover_sound.play()
                hovered_button = "start"
            elif settings_hovered and hovered_button != "settings":
                hover_sound.play()
                hovered_button = "settings"
            elif not start_hovered and not settings_hovered:
                hovered_button = None

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_hovered:
                        click_sound.play()  # Play click sound
                        running = False
                    if settings_hovered:
                        click_sound.play()  # Play click sound
                        self.settings_menu()

            pygame.display.flip()

        reset_game(enemy_manager)
        game_loop(player, enemy_manager)

    def settings_menu(self):
        """Displays the settings menu."""
        running = True

        # Define available resolutions
        resolutions = [(1024, 576), (1280, 720), (1366, 768)]

        # Get the stored resolution, ensuring it is a tuple
        stored_resolution = self.settings.get("resolution", (1366, 768))
        current_resolution = tuple(stored_resolution) if isinstance(stored_resolution, list) else stored_resolution

        # Find the current resolution index, defaulting to (1366, 768) if not found
        if current_resolution not in resolutions:
            current_resolution_index = resolutions.index((1366, 768))
        else:
            current_resolution_index = resolutions.index(current_resolution)

        hovered_button = None

        # Minimum volume threshold (ensures sound is always audible)
        min_volume = 0.01  # 1% volume minimum

        while running:
            self.screen.fill(BLACK)

            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Define volume settings
            options = [
                {"label": "Master Volume", "key": "master_volume"},
                {"label": "Music Volume", "key": "music_volume"},
                {"label": "Effects Volume", "key": "effects_volume"},
            ]

            # Draw sliders for volume settings
            for i, option in enumerate(options):
                label = font_button.render(f"{option['label']}: {self.settings.get(option['key'], 100)}%", True, WHITE)
                slider_x = (self.screen.get_width() - 300) // 2
                slider_y = 150 + i * 100
                slider_width = 300
                slider_height = 20

                pygame.draw.rect(self.screen, GRAY, (slider_x, slider_y, slider_width, slider_height))
                slider_fill_width = int((self.settings[option['key']] / 100) * slider_width)
                pygame.draw.rect(self.screen, GREEN, (slider_x, slider_y, slider_fill_width, slider_height))
                self.screen.blit(label, (slider_x, slider_y - 40))

                # Handle slider interaction
                if pygame.mouse.get_pressed()[0] and slider_x <= mouse_x <= slider_x + slider_width and \
                        slider_y <= mouse_y <= slider_y + slider_height:
                    new_value = int(((mouse_x - slider_x) / slider_width) * 100)
                    self.settings[option['key']] = max(0, min(100, new_value))

                    # Apply volume changes dynamically
                    master_volume = max(self.settings["master_volume"] / 100, min_volume)
                    music_volume = max((self.settings["music_volume"] / 100) * master_volume, min_volume)
                    effects_volume = max((self.settings["effects_volume"] / 100) * master_volume, min_volume)

                    # Adjust music volumes
                    for music, default_vol in {
                        main_menu_music: 0.05,
                        game_music: 0.1,
                        boss_music: 0.1,
                    }.items():
                        if music:
                            music.set_volume(max(default_vol * music_volume, min_volume))

                    # Adjust effects volumes
                    for sound, default_vol in {
                        hover_sound: 0.3,
                        click_sound: 0.3,
                        normal_hit_sound: 0.5,
                        crit_hit_sound: 0.6,
                        collect_xp_sound: 0.5,
                        level_up_sound: 0.5,
                        hurt_sound: 0.5,
                        death_sound: 1.0,
                        ability_obtained_sound: 0.5,
                        ability_used_sound: 0.5,
                        bat_death_sound: 0.05,
                        boss_death_sound: 0.5,
                        skeleton_death_sound: 0.6,
                        blob_death_sound: 1.3,
                        boss_spawn_sound: 0.5,
                    }.items():
                        if sound:
                            sound.set_volume(max(default_vol * effects_volume, min_volume))

            # Resolution Setting with Arrows
            resolution_text = font_button.render(f"{resolutions[current_resolution_index][0]}x{resolutions[current_resolution_index][1]}", True, WHITE)
            res_text_x = (self.screen.get_width() - resolution_text.get_width()) // 2
            res_text_y = 450
            self.screen.blit(resolution_text, (res_text_x, res_text_y))

            # Draw Left Arrow
            if current_resolution_index > 0:
                left_arrow_x = res_text_x - 40
                left_arrow_y = res_text_y + 10
                pygame.draw.polygon(self.screen, WHITE, [
                    (left_arrow_x + 20, left_arrow_y),  # Pointy tip
                    (left_arrow_x, left_arrow_y + 10),  # Bottom
                    (left_arrow_x + 20, left_arrow_y + 20)  # Top
                ])
                if pygame.mouse.get_pressed()[0] and left_arrow_x <= mouse_x <= left_arrow_x + 20 and \
                        left_arrow_y <= mouse_y <= left_arrow_y + 20:
                    current_resolution_index -= 1
                    self.settings["resolution"] = resolutions[current_resolution_index]
                    pygame.display.set_mode(resolutions[current_resolution_index])

            # Draw Right Arrow
            if current_resolution_index < len(resolutions) - 1:
                right_arrow_x = res_text_x + resolution_text.get_width() + 40  # Adjusted spacing
                right_arrow_y = res_text_y + 10
                pygame.draw.polygon(self.screen, WHITE, [
                    (right_arrow_x - 20, right_arrow_y),  # Pointy tip
                    (right_arrow_x, right_arrow_y + 10),  # Bottom
                    (right_arrow_x - 20, right_arrow_y + 20)  # Top
                ])
                if pygame.mouse.get_pressed()[0] and right_arrow_x - 20 <= mouse_x <= right_arrow_x and \
                        right_arrow_y <= mouse_y <= right_arrow_y + 20:
                    current_resolution_index += 1
                    self.settings["resolution"] = resolutions[current_resolution_index]
                    pygame.display.set_mode(resolutions[current_resolution_index])

            # Back Button (Save and Return to Main Menu)
            back_button_x = 20
            back_button_y = self.screen.get_height() - 70
            back_button_width, back_button_height = 150, 50
            back_hovered = back_button_x < mouse_x < back_button_x + back_button_width and \
                        back_button_y < mouse_y < back_button_y + back_button_height
            back_button_color = DARK_RED if back_hovered else RED
            pygame.draw.rect(self.screen, back_button_color, (back_button_x, back_button_y, back_button_width, back_button_height))
            back_text = font_button.render("Back", True, WHITE)
            self.screen.blit(back_text, (
                back_button_x + (back_button_width - back_text.get_width()) // 2,
                back_button_y + (back_button_height - back_text.get_height()) // 2
            ))

            # Play hover sound for the Back button
            if back_hovered and hovered_button != "back":
                hover_sound.play()
                hovered_button = "back"
            elif not back_hovered and hovered_button == "back":
                hovered_button = None

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_hovered:
                        click_sound.play()  # Play click sound
                        self.save_settings()
                        running = False

            pygame.display.flip()

    def game_over_screen(self, score, enemy_manager, reset_game, game_loop):
        """Display the Game Over screen."""
        
        # Stop the game music
        game_music.stop()
        boss_music.stop()

        running = True

        # Update high score if necessary
        if score > self.high_score:
            self.high_score = score
            self.save_high_score(score)

        hovered_button = None  # To track which button is hovered

        while running:
            self.screen.fill(BLACK)

            # Get screen dimensions dynamically
            screen_width = self.screen.get_width()
            screen_height = self.screen.get_height()

            # Display "Game Over" text
            game_over_text = font_title.render("Game Over", True, WHITE)
            self.screen.blit(game_over_text, 
                            (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 4))

            # Display Final Score
            score_text = font_score.render(f"Final Score: {score}", True, WHITE)
            self.screen.blit(score_text, 
                            (screen_width // 2 - score_text.get_width() // 2, screen_height // 4 + 80))

            # Get mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Restart Button
            restart_button_x = screen_width // 2 - 100
            restart_button_y = screen_height // 2
            restart_hovered = restart_button_x < mouse_x < restart_button_x + 200 and \
                            restart_button_y < mouse_y < restart_button_y + 50
            restart_button_color = DARK_RED if restart_hovered else RED
            pygame.draw.rect(self.screen, restart_button_color, 
                            (restart_button_x, restart_button_y, 200, 50))
            restart_text = font_button.render("Restart", True, WHITE)
            self.screen.blit(restart_text, 
                            (restart_button_x + (200 - restart_text.get_width()) // 2, 
                            restart_button_y + (50 - restart_text.get_height()) // 2))

            # Main Menu Button
            menu_button_x = screen_width // 2 - 100
            menu_button_y = restart_button_y + 70
            menu_hovered = menu_button_x < mouse_x < menu_button_x + 200 and \
                        menu_button_y < mouse_y < menu_button_y + 50
            menu_button_color = DARK_RED if menu_hovered else RED
            pygame.draw.rect(self.screen, menu_button_color, 
                            (menu_button_x, menu_button_y, 200, 50))
            menu_text = font_button.render("Main Menu", True, WHITE)
            self.screen.blit(menu_text, 
                            (menu_button_x + (200 - menu_text.get_width()) // 2, 
                            menu_button_y + (50 - menu_text.get_height()) // 2))

            # Play hover sound for buttons
            if restart_hovered and hovered_button != "restart":
                hover_sound.play()
                hovered_button = "restart"
            elif menu_hovered and hovered_button != "menu":
                hover_sound.play()
                hovered_button = "menu"
            elif not restart_hovered and not menu_hovered and hovered_button is not None:
                hovered_button = None

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Restart Button
                    if restart_hovered:
                        click_sound.play()  # Play click sound
                        new_player = Player()  # Create a new player instance
                        reset_game(enemy_manager)  # Reset the game state
                        running = False
                        game_loop(new_player, enemy_manager)
                        return
                    # Main Menu Button
                    if menu_hovered:
                        click_sound.play()  # Play click sound
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
        level_up_sound.play()

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

        hovered_button = None  # To track which button is hovered

        while running:
            self.screen.fill(BLACK)

            # Get dynamic screen dimensions
            screen_width = self.screen.get_width()
            screen_height = self.screen.get_height()

            # Render the title text
            title_text = font_title.render("Level Up!", True, WHITE)
            screen.blit(title_text, (
                screen_width // 2 - title_text.get_width() // 2, 
                screen_height // 4 - 50
            ))

            # Mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Draw buttons and check hover
            button_rects = []  # Store button rects for later click detection
            for i, option in enumerate(selected_upgrades):
                # Button dimensions
                button_width = 350
                button_height = 50
                button_x = screen_width // 2 - button_width // 2
                button_y = screen_height // 4 + 80 + i * 100

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

                # Play hover sound
                if is_hovered and hovered_button != i:
                    hover_sound.play()
                    hovered_button = i
                elif not is_hovered and hovered_button == i:
                    hovered_button = None

                # Add button rect for click detection
                button_rects.append(pygame.Rect(button_x, button_y, button_width, button_height))

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, rect in enumerate(button_rects):
                        if rect.collidepoint(mouse_x, mouse_y):  # Check if click is inside button rect
                            click_sound.play()  # Play click sound
                            player.apply_upgrade(selected_upgrades[i]["upgrade"])
                            running = False  # Exit menu

            pygame.display.flip()

        # Update last_shot_time to avoid firing immediately after exiting the menu
        player.last_shot_time = pygame.time.get_ticks()
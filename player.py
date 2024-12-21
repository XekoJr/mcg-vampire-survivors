import pygame
import time
from settings import *

class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.size = 60
        self.speed = 2
        self.health = 100
        self.xp = 0  # Total XP collected
        self.level = 1  # Starting level
        self.current_xp = 0  # XP toward the next level
        self.xp_to_next_level = 50  # Initial XP required to level up
        self.last_shot_time = 0
        self.score = 0
        self.level_up_pending = False

        # Scaling attributes
        self.fire_rate = fire_rate  # Milliseconds between shots
        self.projectile_damage = 10  # Base projectile damage

        # Carregar as imagens de movimento do jogador
        self.player_images = {
            'down': [pygame.image.load(f'./images/player/down/{i}.png') for i in range(4)],
            'up': [pygame.image.load(f'./images/player/up/{i}.png') for i in range(4)],
            'left': [pygame.image.load(f'./images/player/left/{i}.png') for i in range(4)],
            'right': [pygame.image.load(f'./images/player/right/{i}.png') for i in range(4)],
        }

        # Redimensionar as imagens para o tamanho desejado
        self.player_images = {direction: [pygame.transform.scale(image, (self.size, self.size)) for image in images]
                              for direction, images in self.player_images.items()}

        # Variáveis para controle de animação
        self.animation_index = 0
        self.animation_timer = 0  # Timer para controlar a troca das imagens

        # Inicializar a direção do jogador (começa com "down")
        self.direction = 'down'
        self.animation_index = 0
        
        self.current_image = self.player_images[self.direction][self.animation_index]  # Imagem inicial do jogador
        self.last_move_time = time.time()  # Controle de tempo para animação

        # Controlar a velocidade da animação em segundos
        self.animation_speed = 0.2  # Cada 0.2 segundos troca a imagem
        self.last_animation_time = time.time()  # Marca o tempo da última troca de imagem

    def move(self):
        """Update player movement while respecting map boundaries."""
        keys = pygame.key.get_pressed()
        moving = False  # Variável para verificar se o jogador está se movendo

        # Movimentos para cima (up), para baixo (down), para esquerda (left) e para direita (right)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y = max(0, self.y - self.speed)
            self.direction = 'up'
            moving = True
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y = min(MAP_HEIGHT - self.size, self.y + self.speed)
            self.direction = 'down'
            moving = True
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x = max(0, self.x - self.speed)
            self.direction = 'left'
            moving = True
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x = min(MAP_WIDTH - self.size, self.x + self.speed)
            self.direction = 'right'
            moving = True

        # Atualizar índice de animação apenas se o jogador estiver a mover-se
        if moving:
            current_time = time.time()
            if current_time - self.last_animation_time >= self.animation_speed:
                self.animation_index = (self.animation_index + 1) % len(self.player_images[self.direction])
                self.last_animation_time = current_time

    def gain_xp(self, amount):
        """Add XP and handle leveling up."""
        self.xp += amount
        self.current_xp += amount

        while self.current_xp >= self.xp_to_next_level:
            self.current_xp -= self.xp_to_next_level
            self.level += 1
            self.xp_to_next_level = round(self.xp_to_next_level * 1.5)
            self.level_up_pending = True  # Set flag to trigger level-up menu
            return True
        return False

    def apply_upgrade(self, upgrade):
        if upgrade == "fire_rate":
            self.fire_rate = max(200, self.fire_rate * 0.8)
        elif upgrade == "damage":
            self.projectile_damage *= 1.2
        elif upgrade == "health":
            max_health = 10  # Define a maximum health value
            self.health = min(max_health, self.health + 1)

    def draw(self, screen):
        """Draw the player's current animation frame on the screen."""
        screen.blit(self.player_images[self.direction][self.animation_index], (self.x, self.y))

    def draw_health(self, screen):
        health_text = font_health.render(f"Health: {self.health}", True, WHITE)
        screen.blit(health_text, (10, 10))

    def draw_score(self, screen):
        score_text = font_score.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (WIDTH - 150, 10))

    def draw_xp(self, screen):
        """Draw XP, Level, and XP Progress."""
        xp_text = font_score.render(f"XP: {self.current_xp}/{self.xp_to_next_level}", True, WHITE)
        level_text = font_score.render(f"Level: {self.level}", True, WHITE)
        screen.blit(xp_text, (10, 40))
        screen.blit(level_text, (10, 70))

    def draw_with_offset(self, screen, camera_x, camera_y):
        """Draw player with camera offset."""
        screen.blit(self.player_images[self.direction][self.animation_index], (self.x - camera_x, self.y - camera_y))

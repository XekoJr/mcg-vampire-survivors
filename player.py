import pygame
from settings import WIDTH, HEIGHT, WHITE, BLUE, font_health, font_score, MAP_HEIGHT, MAP_WIDTH

class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.size = 50
        self.speed = 2
        self.health = 3
        self.xp = 0
        self.last_shot_time = 0
        self.score = 0

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y = max(0, self.y - self.speed)  # Prevent moving above the map
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y = min(MAP_HEIGHT - self.size, self.y + self.speed)  # Prevent moving below the map
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x = max(0, self.x - self.speed)  # Prevent moving left of the map
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x = min(MAP_WIDTH - self.size, self.x + self.speed)  # Prevent moving right of the map

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.size, self.size))

    def draw_health(self, screen):
        # Render health text
        health_text = font_health.render(f"Health: {self.health}", True, WHITE)
        screen.blit(health_text, (10, 10))  # Display at the top-left corner

    def draw_score(self, screen):
        score_text = font_score.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (WIDTH - 150, 10))

    def draw_xp(self, screen):
        xp_text = font_score.render(f"XP: {self.xp}", True, WHITE)
        screen.blit(xp_text, (WIDTH - 150, 40))

    def draw_with_offset(self, screen, camera_x, camera_y):
        pygame.draw.rect(screen, BLUE, (self.x - camera_x, self.y - camera_y, self.size, self.size))

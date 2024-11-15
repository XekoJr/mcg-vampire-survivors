import pygame
from settings import *

class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.size = 50
        self.speed = player_speed
        self.health = 3
        self.xp = 0
        self.last_shot_time = 0
        self.score = 0

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.size, self.size))

    def draw_health(self, screen):
        health_text = font_health.render(f"Health: {self.health}", True, WHITE)
        screen.blit(health_text, (10, 10))

    def draw_score(self, screen):
        score_text = font_score.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (WIDTH - 150, 10))

    def draw_xp(self, screen):
        xp_text = font_score.render(f"XP: {self.xp}", True, WHITE)
        screen.blit(xp_text, (WIDTH - 150, 40))

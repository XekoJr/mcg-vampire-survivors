import pygame
from settings import *

# XP properties
xp_size = 10
xp_value = 5  # Amount of XP each drop gives
xp_drops = []  # List to store XP drops
player_xp = 0  # Initial XP

def draw_xp_drops(screen, player):
    player_rect = pygame.Rect(player.x, player.y, player.size, player.size)
    for xp in xp_drops[:]:
        xp_rect = pygame.Rect(xp['x'], xp['y'], xp_size, xp_size)
        pygame.draw.circle(screen, GREEN, (xp['x'], xp['y']), xp_size // 2)
        if player_rect.colliderect(xp_rect):
            player.xp += xp_value
            xp_drops.remove(xp)

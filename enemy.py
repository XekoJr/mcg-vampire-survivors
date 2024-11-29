import pygame
import random
import math
from settings import *

# Lista para armazenar os inimigos
enemies = []

# Carregar imagens para animação
enemy_images = [
    pygame.image.load('./images/enemies/bat/0.png'),
    pygame.image.load('./images/enemies/bat/1.png'),
    pygame.image.load('./images/enemies/bat/2.png'),
    pygame.image.load('./images/enemies/bat/3.png')
]

# Redimensionar as imagens para o tamanho desejado
enemy_images = [pygame.transform.scale(image, (50, 50)) for image in enemy_images]

# Variável para controlar a troca de imagens do inimigo
enemy_animation_index = 0
enemy_animation_timer = 0  # Timer para controlar a troca das imagens

def spawn_enemy():
    # Randomly choose a side: 0 = top, 1 = bottom, 2 = left, 3 = right
    side = random.randint(0, 3)

    if side == 0:  # Top edge
        x = random.randint(0, MAP_WIDTH - 40)
        y = -40
    elif side == 1:  # Bottom edge
        x = random.randint(0, MAP_WIDTH - 40)
        y = MAP_HEIGHT
    elif side == 2:  # Left edge
        x = -40
        y = random.randint(0, MAP_HEIGHT - 40)
    else:  # Right edge
        x = MAP_WIDTH
        y = random.randint(0, MAP_HEIGHT - 40)

    # Add the new enemy to the list
    enemy_hp = 20  # Health points of the enemy
    enemies.append({'x': x, 'y': y, 'hp': enemy_hp})

def draw_enemies(screen, camera_x, camera_y):
    global enemy_animation_index, enemy_animation_timer

    # A cada 100 ms, troca a imagem
    enemy_animation_timer += 1
    if enemy_animation_timer >= 5:  # Troca de imagem a cada 5 quadros
        enemy_animation_index = (enemy_animation_index + 1) % len(enemy_images)
        enemy_animation_timer = 0  # Reset timer

    for enemy in enemies:
        max_hp = 20  # Máximo de HP do inimigo
        health_ratio = max(0, enemy['hp'] / max_hp)  # Calcula a proporção do HP restante

        # A cor da barra de HP (de vermelho a verde)
        if health_ratio > 0.6:
            color = GREEN
        elif health_ratio > 0.3:
            color = YELLOW
        else:
            color = RED
        # Desenha a barra de fundo da vida do inimigo (preta), sempre do mesmo tamanho
        pygame.draw.rect(screen, BLACK, (
            enemy['x'] - camera_x,
            enemy['y'] - camera_y - 10,
            40, 5  # Comprimento fixo da barra de HP
        ))

        # Desenha a parte do HP do inimigo (a parte interna, que muda de cor)
        pygame.draw.rect(screen, color, (
            enemy['x'] - camera_x,
            enemy['y'] - camera_y - 10,
            40 * health_ratio, 5  # O comprimento da barra depende do HP restante
        ))

        # Desenha a imagem do inimigo na tela
        screen.blit(enemy_images[enemy_animation_index], (
            enemy['x'] - camera_x,
            enemy['y'] - camera_y
        ))

def move_enemies(player_x, player_y):
    for enemy in enemies:
        dx = player_x - enemy['x']
        dy = player_y - enemy['y']
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 0:
            dx /= distance
            dy /= distance
        enemy['x'] += dx
        enemy['y'] += dy

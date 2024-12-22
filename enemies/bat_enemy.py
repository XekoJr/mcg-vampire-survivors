from enemies.enemy import Enemy
import pygame

class BatEnemy(Enemy):
    """Basic flying bat enemy."""
    def __init__(self, x, y):
        # Load images specific to BatEnemy
        images = [
            pygame.image.load('./assets/images/enemies/bat/0.png'),
            pygame.image.load('./assets/images/enemies/bat/1.png'),
            pygame.image.load('./assets/images/enemies/bat/2.png'),
            pygame.image.load('./assets/images/enemies/bat/3.png')
        ]
        super().__init__(x, y, hp=20, speed=1.5, size=(50, 50), images=images)
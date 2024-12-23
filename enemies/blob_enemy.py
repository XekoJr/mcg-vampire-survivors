from enemies.enemy import Enemy
import pygame

class BlobEnemy(Enemy):
    """Slow but high-health tank enemy."""
    def __init__(self, x, y):
        # Load images specific to TankEnemy
        images = [
            pygame.image.load('./assets/images/enemies/blob/0.png'),
            pygame.image.load('./assets/images/enemies/blob/1.png'),
            pygame.image.load('./assets/images/enemies/blob/2.png'),
            pygame.image.load('./assets/images/enemies/blob/3.png')
        ]
        super().__init__(x, y, hp=50, speed=0.8, xp_value=20, damage=50, size=(80, 70), images=images)
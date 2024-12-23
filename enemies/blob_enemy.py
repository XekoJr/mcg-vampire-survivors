from enemies.enemy import Enemy
import pygame

class BlobEnemy(Enemy):
    """Slow but high-health tank enemy."""
    def __init__(self, x, y):
        # Load images specific to TankEnemy
        images = [
            pygame.image.load(f'./assets/images/enemies/blob/{i}.png') for i in range(4)
        ]
        super().__init__(x, y, hp=50, speed=0.8, xp_value=20, damage=50, size=(80, 70), images=images)
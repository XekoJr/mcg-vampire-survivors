import pygame
import time
from abilities.ability import Ability

class ShieldAbility(Ability):
    """An ability that blocks one incoming attack and resets after a cooldown."""
    def __init__(self, name="Block Shield", 
                 description="Block one incoming attack and resets after 30 seconds.", 
                 cost=5, 
                 icon_path='./assets/images/abilities/shield.png', 
                 images=[]
                 ):
        super().__init__(name, description, cost, icon_path, images, active=False)
        self.ready = True  # Tracks whether the ability is ready to block an attack
        self.blocked = False  # Tracks whether the ability has blocked an attack
        self.cooldown = 30  # Cooldown duration in seconds
        self.last_block_time = None  # Tracks the last time the ability blocked an attack

    def block(self):
        """Block one attack and deactivate the ability."""
        if self.active and self.ready:
            self.blocked = True
            self.ready = False
            self.last_block_time = time.time()
            return True
        return False

    def update(self):
        """Check if the cooldown has passed and reset the block ability."""
        if not self.ready:
            current_time = time.time()
            if self.last_block_time is not None:
                elapsed_time = current_time - self.last_block_time
                if elapsed_time >= self.cooldown:
                    self.reset_block()

    def reset_block(self):
        """Reset the block ability, allowing it to be used again."""
        self.blocked = False
        self.last_block_time = None
        self.ready = True

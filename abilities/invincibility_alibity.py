import pygame
from abilities.ability import Ability

class InvincibilityAbility(Ability):
    """An ability that increases the invincibility duration after taking damage."""
    def __init__(self, name="Invincibility Boost",
                 description="Increase invincibility duration after taking damage.",
                 cost=6,
                 icon_path='./assets/images/abilities/invincibility.png',
                 images=[],
                 level=1  # Default level
                 ):
        super().__init__(name, description, cost, icon_path, images, active=False)
        self.level = level  # Ability level
        self.base_additional_invincibility_time = 0.2  # Base increment per level

    def apply_invincibility(self, player):
        """Increase the player's invincibility duration based on ability level."""
        if self.active:
            additional_time = self.base_additional_invincibility_time * self.level
            player.invincibility_time = max(
                player.invincibility_time, 
                player.base_invincibility_time + additional_time
            )

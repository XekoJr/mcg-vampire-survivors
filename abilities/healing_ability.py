import pygame
import time

from abilities.ability import Ability

class HealingAbility(Ability):
    """An ability that passively heals the player for 5 HP every 10 seconds."""
    def __init__(self, name="Healing Aura", 
                 description="Heal 5 HP every 10 seconds", 
                 cost=5, 
                 icon_path='./assets/images/abilities/heal.png', 
                 images=[]
                 ):
        super().__init__(name, description, cost, icon_path, images, active=False)
        self.last_heal_time = 0  # Tracks the last time the ability healed
        self.heal_amount = 5  # Amount of HP healed
        self.cooldown = 10  # Cooldown time in seconds for healing

    def heal(self, player):
        """Heal the player if the cooldown period has passed."""
        current_time = time.time()
        if self.active and (current_time - self.last_heal_time >= self.cooldown):
            # Heal the player
            player.health = min(player.max_health, player.health + self.heal_amount)
            self.last_heal_time = current_time  # Update the last heal time

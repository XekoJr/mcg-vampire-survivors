import pygame
import time
from abilities.ability import Ability

class PoisonAbility(Ability):
    """An ability that poisons the target, dealing 1 damage every 2 seconds for 6 seconds."""
    def __init__(self, name="Poison Touch", 
                 description="Poison the target, dealing 0.4 damage every 1 second for 10 seconds.", 
                 cost=4, 
                 icon_path='./assets/images/abilities/poison.png', 
                 images=[]
                 ):
        super().__init__(name, description, cost, icon_path, images, active=False)
        self.poison_damage = 0.4  # Damage dealt every tick
        self.poison_duration = 10  # Duration of the poison in seconds
        self.poison_interval = 1  # Time between poison ticks in seconds
        self.last_poison_time = {}  # Dictionary to track the last poison tick per target

    def poison(self, target):
        """Apply poison to a target."""
        if self.active and target not in self.last_poison_time:
            # Initialize poison tracking for the target
            self.last_poison_time[target] = {
                "start_time": time.time(),
                "next_tick": time.time() + self.poison_interval,
                "ticks_left": self.poison_duration // self.poison_interval,
            }

    def update_poison(self, targets):
        """Deal poison damage to targets and remove poison when finished."""
        current_time = time.time()
        for target in list(self.last_poison_time.keys()):  # Use a list to avoid modifying during iteration
            poison_data = self.last_poison_time[target]
            if current_time >= poison_data["next_tick"]:
                # Deal poison damage
                target.hp -= self.poison_damage
                
                # Update for the next tick
                poison_data["next_tick"] += self.poison_interval
                poison_data["ticks_left"] -= 1

                # Remove poison if duration is over
                if poison_data["ticks_left"] <= 0 or target.hp <= 0:
                    del self.last_poison_time[target]  # Clean up poison tracking
                    continue

                # Check if the target died from poison
                if target.hp <= 0:
                    if target in self.last_poison_time:
                        del self.last_poison_time[target]  # Avoid errors if already removed
                    continue

    def __str__(self):
        return f"{self.name} - {self.description} (Cost: {self.cost}, Bought: {self.bought}, Equipped: {self.equipped}, Active: {self.active})"

import time
from abilities.ability import Ability

class PoisonAbility(Ability):
    """An ability that applies a poison effect, dealing damage over time."""
    def __init__(self, name="Poison Touch",
                 description="Apply poison to enemies, dealing damage over time.",
                 cost=4,
                 icon_path='./assets/images/abilities/poison.png',
                 images=[]
                 ):
        super().__init__(name, description, cost, icon_path, images, active=False)
        self.base_poison_damage = 0.4  # Base damage dealt per tick
        self.base_poison_duration = 10  # Base duration of the poison in seconds
        self.poison_interval = 1  # Time between poison ticks in seconds
        self.poison_damage = self.base_poison_damage
        self.poison_duration = self.base_poison_duration

    def apply_poison(self, enemy):
        """Apply the poison effect to an enemy."""
        current_time = time.time()
        if not hasattr(enemy, "poison_end_time") or current_time > enemy.poison_end_time:
            enemy.poison_end_time = current_time + self.poison_duration
            enemy.next_poison_tick = current_time

    def update_poison(self, enemy):
        """Update the poison effect, dealing damage at regular intervals."""
        current_time = time.time()
        if hasattr(enemy, "poison_end_time") and current_time <= enemy.poison_end_time:
            if current_time >= enemy.next_poison_tick:
                enemy.take_damage(self.poison_damage)
                enemy.next_poison_tick += self.poison_interval

                # Check if the enemy is dead
                if enemy.hp <= 0:
                    return True  # Indicate the enemy is dead
        elif hasattr(enemy, "poison_end_time") and current_time > enemy.poison_end_time:
            del enemy.poison_end_time
            del enemy.next_poison_tick
        return False

    """
    def update_attributes(self, poison_damage_level, poison_duration_level):
        #Update the poison damage and duration based on skill levels.
        self.poison_damage = self.base_poison_damage + (0.2 * poison_damage_level)
        self.poison_duration = self.base_poison_duration + (1 * poison_duration_level)
    """

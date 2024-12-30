import time
from abilities.ability import Ability

class BurningAbility(Ability):
    """An ability that applies a burning effect, dealing damage over time."""
    def __init__(self, name="Burning Touch",
                 description="Apply burning to enemies, dealing 0.8 damage every 0.5 seconds for 3 seconds.",
                 cost=5,
                 icon_path='./assets/images/abilities/burn.png',
                 images=[]
                 ):
        super().__init__(name, description, cost, icon_path, images, active=False)
        self.burn_damage = 0.8  # Base damage dealt every tick
        self.burn_duration = 3  # Base duration of the burn in seconds
        self.burn_interval = 0.5  # Time interval between burn ticks
        self.burn_cooldown = 5  # Time before the same enemy can be burned again

    def apply_burn(self, enemy):
        """Apply a burning effect to an enemy."""
        current_time = time.time()

        # Check if the enemy is on cooldown
        if hasattr(enemy, "burn_cooldown_end_time") and current_time < enemy.burn_cooldown_end_time:
            return

        if self.active:
            # Start the burn effect
            if not hasattr(enemy, "burn_end_time") or current_time > enemy.burn_end_time:
                enemy.burn_end_time = current_time + self.burn_duration
                enemy.next_burn_tick = current_time

    def update_burn(self, enemy):
        """Update the burning effect, dealing damage at regular intervals."""
        if hasattr(enemy, "burn_end_time") and time.time() <= enemy.burn_end_time:
            current_time = time.time()
            if current_time >= enemy.next_burn_tick:
                # Apply burn damage
                enemy.take_damage(self.burn_damage)
                enemy.next_burn_tick += self.burn_interval

        # Check if the burn effect has ended
        if hasattr(enemy, "burn_end_time") and time.time() > enemy.burn_end_time:
            del enemy.burn_end_time
            del enemy.next_burn_tick

            # Start the cooldown for the enemy
            enemy.burn_cooldown_end_time = time.time() + self.burn_cooldown

    def update_attributes(self, burn_damage_level, burn_duration_level):
        """Update the attributes of the burning ability based on skill levels."""
        self.burn_damage = 0.8 + (0.2 * burn_damage_level)  # Example scaling: +0.2 per level
        self.burn_duration = 3 + (0.5 * burn_duration_level)  # Example scaling: +0.5 seconds per level

import pygame

class Ability:
    """Base class for abilities."""
    def __init__(self, name, description, cost, icon_path=None, images=None, active=False):
        self.name = name  # Ability name
        self.description = description  # Short description of what the ability does
        self.cost = cost  # Cost to unlock or upgrade the ability
        self.icon_path = icon_path  # Path to the ability icon
        self.images = images if images else []  # List of images for animations
        self.active = active  # Whether the ability is currently active

    def draw_icon(self, screen, x, y, size=35):
        """Draw the ability icon dynamically."""
        if self.icon_path:
            try:
                # Load and scale the icon
                icon = pygame.image.load(self.icon_path)
                icon = pygame.transform.scale(icon, (size, size))
                screen.blit(icon, (x, y))
            except FileNotFoundError:
                print(f"[DEBUG] Icon file not found for {self.name}: {self.icon_path}")
        else:
            print(f"[DEBUG] No icon path specified for {self.name}")

    def activate(self):
        """Activate the ability."""
        self.active = True

    def deactivate(self):
        """Deactivate the ability."""
        self.active = False

    def __str__(self):
        return f"{self.name} - {self.description} (Cost: {self.cost}, Active: {self.active})"

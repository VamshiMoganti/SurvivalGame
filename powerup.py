import pygame
import random
import math
from settings import POWERUP_SIZE, POWERUP_SPEED, WIDTH, GREEN, YELLOW
from sprites import PowerUpVisual

class PowerUp:
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.size = POWERUP_SIZE
        self.speed = POWERUP_SPEED
        self.power_type = power_type  # 'health' or 'fire_rate'
        self.color = GREEN if power_type == 'health' else YELLOW
        self.pulse = 0
        self.rotation = 0

    def update(self):
        self.y += self.speed
        self.pulse = abs(math.sin(self.pulse + 0.1))
        self.rotation = (self.rotation + 5) % 360

    def draw(self, screen):
        if self.power_type == 'health':
            PowerUpVisual.draw_health_powerup(screen, int(self.x), int(self.y), self.size, self.pulse)
        else:
            PowerUpVisual.draw_firerate_powerup(screen, int(self.x), int(self.y), self.size, self.pulse)

    def off_screen(self):
        return self.y > 600

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

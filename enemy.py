import pygame
import random
from settings import ENEMY_SIZE, ENEMY_SPEED, RED, WIDTH

class Enemy:
    def __init__(self):
        self.x = random.randint(0, WIDTH - ENEMY_SIZE)
        self.y = -ENEMY_SIZE
        self.size = ENEMY_SIZE
        self.speed = ENEMY_SPEED

    def update(self):
        self.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.size, self.size))

    def off_screen(self):
        return self.y > 600

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

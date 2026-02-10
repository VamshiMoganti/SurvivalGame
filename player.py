import pygame
from settings import PLAYER_SIZE, PLAYER_SPEED, BLUE, WIDTH, HEIGHT

class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.size = PLAYER_SIZE
        self.speed = PLAYER_SPEED

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.size:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < HEIGHT - self.size:
            self.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.size, self.size))

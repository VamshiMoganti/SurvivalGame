import pygame

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 5
        self.height = 10
        self.speed = 10

    def update(self):
        self.y -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height))

    def off_screen(self):
        return self.y < 0

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

import pygame
from sprites import BulletVisual

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 5
        self.height = 10
        self.speed = 10
        self.trail_points = [(x, y)]
        self.max_trail_length = 15

    def update(self):
        self.y -= self.speed
        self.trail_points.append((self.x, self.y))
        if len(self.trail_points) > self.max_trail_length:
            self.trail_points.pop(0)

    def draw(self, screen):
        BulletVisual.draw_bullet(screen, self.x, self.y, self.width, self.height, self.trail_points)

    def off_screen(self):
        return self.y < 0

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

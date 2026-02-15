import pygame
import random
import math
from settings import ENEMY_SIZE, ENEMY_SPEED, RED, WIDTH, ORANGE, YELLOW

class Boss:
    """Boss enemy - appears every 50 points"""
    def __init__(self):
        self.x = WIDTH // 2 - 75
        self.y = -150
        self.size = 150
        self.speed = 1
        self.health = 20
        self.max_health = 20
        self.enemy_type = 'boss'
        self.color = (200, 0, 255)
        self.spawn_animation = 0
        self.spawn_animation_max = 20
        self.damage_flash = 0
        self.attack_cooldown = 0
        self.shoot_bullets = []

    def update(self):
        # Move into position
        if self.y < 100:
            self.y += self.speed
        
        if self.spawn_animation < self.spawn_animation_max:
            self.spawn_animation += 1
        
        if self.damage_flash > 0:
            self.damage_flash -= 1
        
        # Oscillate left and right
        if self.y >= 100:
            offset = math.sin(pygame.time.get_ticks() / 500) * 100
            self.x = max(0, min(WIDTH - self.size, WIDTH // 2 - self.size // 2 + offset))
        
        self.attack_cooldown -= 1

    def draw(self, screen):
        # Spawn animation - scale up
        scale = self.spawn_animation / self.spawn_animation_max if self.spawn_animation < self.spawn_animation_max else 1.0
        draw_size = int(self.size * scale)
        draw_x = self.x + (self.size - draw_size) // 2
        draw_y = self.y + (self.size - draw_size) // 2
        
        # Draw damage flash
        if self.damage_flash > 0:
            flash_color = (255, 255, 255)
            pygame.draw.rect(screen, flash_color, (draw_x, draw_y, draw_size, draw_size))
        
        # Main body
        pygame.draw.rect(screen, self.color, (draw_x, draw_y, draw_size, draw_size))
        
        # Eyes
        eye_size = max(3, int(draw_size // 10))
        pygame.draw.circle(screen, (255, 0, 0), (int(draw_x + draw_size * 0.3), int(draw_y + draw_size * 0.3)), eye_size)
        pygame.draw.circle(screen, (255, 0, 0), (int(draw_x + draw_size * 0.7), int(draw_y + draw_size * 0.3)), eye_size)
        
        # Crown
        crown_points = [
            (draw_x + draw_size // 2, draw_y - 20),
            (draw_x + draw_size // 4, draw_y + 10),
            (draw_x + draw_size * 0.4, draw_y),
            (draw_x + draw_size // 2, draw_y - 10),
            (draw_x + draw_size * 0.6, draw_y),
            (draw_x + draw_size * 0.75, draw_y + 10)
        ]
        if len(crown_points) > 2:
            pygame.draw.polygon(screen, (255, 215, 0), crown_points)
        
        # Draw health bar
        bar_width = self.size
        bar_height = 10
        pygame.draw.rect(screen, (100, 0, 0), (self.x, self.y - 20, bar_width, bar_height))
        health_ratio = self.health / self.max_health
        health_color = (255, 0, 0) if health_ratio > 0.5 else (255, 100, 0)
        pygame.draw.rect(screen, health_color, (self.x, self.y - 20, bar_width * health_ratio, bar_height))
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y - 20, bar_width, bar_height), 2)
        
        # Boss label
        font = pygame.font.SysFont(None, 24)
        boss_text = font.render("BOSS", True, (255, 0, 255))
        screen.blit(boss_text, (self.x + self.size // 2 - 15, self.y - 50))

    def off_screen(self):
        return self.y > 700

    def get_rect(self):
        scale = self.spawn_animation / self.spawn_animation_max if self.spawn_animation < self.spawn_animation_max else 1.0
        draw_size = int(self.size * scale)
        draw_x = self.x + (self.size - draw_size) // 2
        draw_y = self.y + (self.size - draw_size) // 2
        return pygame.Rect(draw_x, draw_y, draw_size, draw_size)

    def take_damage(self, amount=1):
        self.health -= amount
        self.damage_flash = 5
        return self.health <= 0

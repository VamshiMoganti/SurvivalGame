import pygame
import random
import math
from settings import ENEMY_SIZE, ENEMY_SPEED, RED, WIDTH, ORANGE, YELLOW
from space_graphics import AsteroidGraphics, UFOGraphics

class Enemy:
    def __init__(self):
        self.x = random.randint(0, WIDTH - ENEMY_SIZE)
        self.y = -ENEMY_SIZE
        self.size = ENEMY_SIZE
        self.speed = ENEMY_SPEED
        self.enemy_type = 'basic'  # basic, fast, tanky, spawner, drone
        self.health = 1
        self.max_health = 1
        self.color = RED
        self.spawn_animation = 0
        self.spawn_animation_max = 10
        self.damage_flash = 0
        self.health_display_cooldown = 0

    def update(self):
        self.y += self.speed
        if self.spawn_animation < self.spawn_animation_max:
            self.spawn_animation += 1
        if self.damage_flash > 0:
            self.damage_flash -= 1
        if self.health_display_cooldown > 0:
            self.health_display_cooldown -= 1

    def draw(self, screen):
        # Spawn animation - scale up
        scale = self.spawn_animation / self.spawn_animation_max
        draw_size = int(self.size * scale)
        draw_x = self.x + (self.size - draw_size) // 2
        draw_y = self.y + (self.size - draw_size) // 2
        
        # Draw damage flash
        if self.damage_flash > 0:
            flash_color = (255, 255, 255)
            pygame.draw.circle(screen, flash_color, (int(draw_x + draw_size // 2), int(draw_y + draw_size // 2)), draw_size // 2)
        
        # Draw enemy sprite based on type
        health_ratio = self.health / self.max_health
        try:
            if self.enemy_type == 'basic':
                AsteroidGraphics.draw_small_asteroid(screen, draw_x, draw_y, draw_size)
            elif self.enemy_type == 'fast':
                AsteroidGraphics.draw_medium_asteroid(screen, draw_x, draw_y, int(draw_size * 0.75))
            elif self.enemy_type == 'tanky':
                AsteroidGraphics.draw_large_asteroid(screen, draw_x, draw_y, int(draw_size * 1.3))
            elif self.enemy_type == 'spawner':
                UFOGraphics.draw_scout_ufo(screen, draw_x, draw_y, draw_size)
            elif self.enemy_type == 'drone':
                UFOGraphics.draw_scout_ufo(screen, draw_x, draw_y, int(draw_size * 0.6))
        except Exception as e:
            # Fallback to basic asteroid if drawing fails
            pygame.draw.circle(screen, (200, 100, 50), (int(draw_x + draw_size // 2), int(draw_y + draw_size // 2)), draw_size // 2)
        
        # Draw health bar only if multi-health and visible
        if self.max_health > 1 and self.health_display_cooldown > 0:
            bar_width = self.size
            bar_height = 5
            # Background bar (dark)
            pygame.draw.rect(screen, (50, 20, 20), (self.x, self.y - 15, bar_width, bar_height))
            # Health bar (colored by health percentage)
            health_color = (0, 255, 0) if health_ratio > 0.66 else (255, 200, 0) if health_ratio > 0.33 else (255, 0, 0)
            pygame.draw.rect(screen, health_color, (self.x, self.y - 15, bar_width * health_ratio, bar_height))
            pygame.draw.rect(screen, (150, 150, 150), (self.x, self.y - 15, bar_width, bar_height), 1)

    def off_screen(self):
        return self.y > 600

    def get_rect(self):
        # Spawn animation affects hitbox
        scale = self.spawn_animation / self.spawn_animation_max
        draw_size = int(self.size * scale)
        draw_x = self.x + (self.size - draw_size) // 2
        draw_y = self.y + (self.size - draw_size) // 2
        return pygame.Rect(draw_x, draw_y, draw_size, draw_size)

    def take_damage(self, amount=1):
        self.health -= amount
        self.damage_flash = 5  # Flash for 5 frames
        self.health_display_cooldown = 60  # Show health bar for 60 frames after taking damage
        return self.health <= 0


def create_random_enemy():
    """Create an enemy with random type"""
    # 60% basic, 20% fast, 10% tanky, 7% spawner, 3% drone
    enemy_type = random.choices(
        ['basic', 'fast', 'tanky', 'spawner', 'drone'], 
        weights=[60, 20, 10, 7, 3]
    )[0]
    
    enemy = Enemy()
    
    if enemy_type == 'fast':
        enemy.enemy_type = 'fast'
        enemy.speed = ENEMY_SPEED * 1.8
        enemy.color = YELLOW
        enemy.size = int(ENEMY_SIZE * 0.75)
        enemy.health = 1
        enemy.max_health = 1
    
    elif enemy_type == 'tanky':
        enemy.enemy_type = 'tanky'
        enemy.speed = ENEMY_SPEED * 0.5
        enemy.color = ORANGE
        enemy.size = int(ENEMY_SIZE * 1.3)
        enemy.health = 3
        enemy.max_health = 3
    
    elif enemy_type == 'spawner':
        enemy.enemy_type = 'spawner'
        enemy.speed = ENEMY_SPEED * 0.3
        enemy.color = (200, 50, 200)  # Purple
        enemy.size = int(ENEMY_SIZE * 1.2)
        enemy.health = 2
        enemy.max_health = 2
        enemy.spawn_cooldown = 120
    
    elif enemy_type == 'drone':
        enemy.enemy_type = 'drone'
        enemy.speed = ENEMY_SPEED * 1.5
        enemy.color = (0, 200, 255)  # Cyan
        enemy.size = int(ENEMY_SIZE * 0.6)
        enemy.health = 1
        enemy.max_health = 1
        enemy.wave_offset = random.randint(0, 100)
    
    return enemy


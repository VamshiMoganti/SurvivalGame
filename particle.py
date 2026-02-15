import pygame
import random
import math

class Particle:
    def __init__(self, x, y, color, velocity, lifetime=30):
        self.x = x
        self.y = y
        self.color = color
        self.vx = velocity[0]
        self.vy = velocity[1]
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = 5

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        self.vy += 0.2  # Gravity effect

    def draw(self, screen):
        # Fade out particle
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        fade_color = tuple(int(c * (self.lifetime / self.max_lifetime)) for c in self.color)
        pygame.draw.circle(screen, fade_color, (int(self.x), int(self.y)), max(1, int(self.size * (self.lifetime / self.max_lifetime))))

    def is_alive(self):
        return self.lifetime > 0


class Explosion:
    def __init__(self, x, y, color=(255, 165, 0), particle_count=15):
        self.particles = []
        for _ in range(particle_count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            self.particles.append(Particle(x, y, color, (vx, vy), lifetime=random.randint(20, 40)))

    def update(self):
        for particle in self.particles[:]:
            particle.update()
            if not particle.is_alive():
                self.particles.remove(particle)

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)

    def is_done(self):
        return len(self.particles) == 0


class FloatingText:
    def __init__(self, x, y, text, color, lifetime=60):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.velocity_y = -2

    def update(self):
        self.y += self.velocity_y
        self.lifetime -= 1

    def draw(self, screen, font):
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        fade_color = tuple(int(c * (self.lifetime / self.max_lifetime)) for c in self.color)
        
        text_surface = font.render(self.text, True, fade_color)
        screen.blit(text_surface, (int(self.x), int(self.y)))

    def is_alive(self):
        return self.lifetime > 0

class CritHitEffect:
    """Visual effect for critical hits - yellow star burst"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lifetime = 20
        self.max_lifetime = 20
        self.particles = []
        for _ in range(8):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 6)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            self.particles.append(Particle(x, y, (255, 255, 0), (vx, vy), 20))

    def update(self):
        self.lifetime -= 1
        for p in self.particles:
            p.update()

    def draw(self, screen):
        for p in self.particles:
            p.draw(screen)

    def is_done(self):
        return self.lifetime <= 0


class WaveEffect:
    """Screen wave effect for special events"""
    def __init__(self, center_x, center_y, max_radius=300):
        self.center_x = center_x
        self.center_y = center_y
        self.lifetime = 40
        self.max_lifetime = 40
        self.max_radius = max_radius
        self.wave_width = 20

    def update(self):
        self.lifetime -= 1

    def draw(self, screen):
        progress = 1 - (self.lifetime / self.max_lifetime)
        radius = progress * self.max_radius
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        
        # Draw expanding circle waves
        pygame.draw.circle(screen, (0, 255, 255), (int(self.center_x), int(self.center_y)), int(radius), 3)
        pygame.draw.circle(screen, (100, 200, 255), (int(self.center_x), int(self.center_y)), int(radius) - 10, 1)

    def is_done(self):
        return self.lifetime <= 0


class LootEffect:
    """Gold/shimmer effect for power-ups"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lifetime = 30
        self.max_lifetime = 30
        self.particles = []
        for _ in range(12):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 4)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed - 1  # Bias upward
            self.particles.append(Particle(x, y, (255, 200, 0), (vx, vy), 30))

    def update(self):
        self.lifetime -= 1
        for p in self.particles:
            p.update()

    def draw(self, screen):
        for p in self.particles:
            p.draw(screen)

    def is_done(self):
        return self.lifetime <= 0
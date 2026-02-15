import pygame
import math

class PlayerAvatar:
    """Different player avatar types with unique visuals"""
    
    @staticmethod
    def draw_knight(screen, x, y, size, color=(100, 150, 255)):
        """Knight avatar - armored warrior"""
        # Body
        pygame.draw.rect(screen, color, (x, y + size // 4, size, size // 2))
        # Head
        pygame.draw.circle(screen, (220, 180, 100), (x + size // 2, y + size // 6), size // 4)
        # Helmet
        pygame.draw.polygon(screen, (150, 150, 150), [
            (x + size // 2, y),
            (x + size // 4, y + size // 3),
            (x + 3 * size // 4, y + size // 3)
        ])
        # Eyes
        pygame.draw.circle(screen, (0, 0, 0), (x + size // 3, y + size // 6), 2)
        pygame.draw.circle(screen, (0, 0, 0), (x + 2 * size // 3, y + size // 6), 2)
        # Shield pattern
        pygame.draw.rect(screen, (200, 50, 50), (x + size // 4, y + size // 3, size // 2, size // 3), 2)
    
    @staticmethod
    def draw_wizard(screen, x, y, size, color=(180, 100, 255)):
        """Wizard avatar - magical caster"""
        # Body
        pygame.draw.polygon(screen, color, [
            (x + size // 2, y),
            (x + size // 4, y + size // 2),
            (x + 3 * size // 4, y + size // 2)
        ])
        # Cape
        pygame.draw.polygon(screen, (100, 50, 150), [
            (x + size // 4, y + size // 2),
            (x, y + size),
            (x + size, y + size),
            (x + 3 * size // 4, y + size // 2)
        ])
        # Hat
        pygame.draw.polygon(screen, (150, 100, 200), [
            (x + size // 2, y - size // 4),
            (x + size // 4, y + size // 4),
            (x + 3 * size // 4, y + size // 4)
        ])
        # Star on hat
        pygame.draw.circle(screen, (255, 255, 0), (x + size // 2, y), 3)
    
    @staticmethod
    def draw_ninja(screen, x, y, size, color=(40, 40, 40)):
        """Ninja avatar - stealthy fighter"""
        # Body
        pygame.draw.rect(screen, color, (x + size // 4, y + size // 4, size // 2, size // 2))
        # Head
        pygame.draw.circle(screen, (30, 30, 30), (x + size // 2, y + size // 6), size // 5)
        # Mask
        pygame.draw.rect(screen, (255, 0, 0), (x + size // 3, y + size // 8, size // 3, size // 6))
        # Eyes glow
        pygame.draw.circle(screen, (255, 255, 0), (x + size // 3 + 2, y + size // 6), 2)
        pygame.draw.circle(screen, (255, 255, 0), (x + size // 2 + 4, y + size // 6), 2)
        # Throwing stars effect
        for i in range(3):
            angle = i * math.pi / 1.5
            star_x = x + size // 2 + math.cos(angle) * size // 3
            star_y = y + size // 2 + math.sin(angle) * size // 3
            pygame.draw.circle(screen, (200, 0, 0), (int(star_x), int(star_y)), 2)
    
    @staticmethod
    def draw_robot(screen, x, y, size, color=(150, 150, 150)):
        """Robot avatar - mechanical fighter"""
        # Body
        pygame.draw.rect(screen, color, (x + size // 4, y + size // 3, size // 2, size // 2))
        # Head
        pygame.draw.rect(screen, (180, 180, 180), (x + size // 4, y, size // 2, size // 3))
        # Left eye
        pygame.draw.rect(screen, (0, 255, 0), (x + size // 3, y + size // 8, size // 8, size // 8))
        # Right eye
        pygame.draw.rect(screen, (0, 255, 0), (x + size // 2 + size // 12, y + size // 8, size // 8, size // 8))
        # Antenna
        pygame.draw.line(screen, (200, 0, 255), (x + size // 2, y), (x + size // 2, y - size // 4), 2)
        pygame.draw.circle(screen, (200, 0, 255), (x + size // 2, y - size // 4), 3)
    
    @staticmethod
    def draw_phoenix(screen, x, y, size, color=(255, 100, 0)):
        """Phoenix avatar - fiery bird"""
        # Body
        pygame.draw.circle(screen, color, (x + size // 2, y + size // 2), size // 3)
        # Head
        pygame.draw.circle(screen, (255, 150, 0), (x + size // 2, y + size // 4), size // 5)
        # Beak
        pygame.draw.polygon(screen, (255, 200, 0), [
            (x + size // 2 + size // 5, y + size // 4),
            (x + size // 2 + size // 2, y + size // 4),
            (x + size // 2 + size // 4, y + size // 3)
        ])
        # Flames
        for i in range(4):
            flame_x = x + size // 2 + math.cos(i * math.pi / 2) * size // 2
            flame_y = y + size // 2 + math.sin(i * math.pi / 2) * size // 2
            pygame.draw.polygon(screen, (255, 50, 0), [
                (int(flame_x), int(flame_y)),
                (int(flame_x) - 3, int(flame_y) - 5),
                (int(flame_x) + 3, int(flame_y) - 5)
            ])


class EnemySprite:
    """Different enemy sprite types"""
    
    @staticmethod
    def draw_basic_enemy(screen, x, y, size, health_ratio=1.0):
        """Basic enemy - simple alien"""
        # Body
        pygame.draw.polygon(screen, (255, 0, 0), [
            (x + size // 2, y),
            (x + size, y + size // 2),
            (x + size // 2, y + size),
            (x, y + size // 2)
        ])
        # Eyes
        pygame.draw.circle(screen, (0, 0, 0), (x + size // 3, y + size // 3), 3)
        pygame.draw.circle(screen, (0, 0, 0), (x + 2 * size // 3, y + size // 3), 3)
        # Eye glow based on health
        glow_colors = [(255, 255, 255), (255, 200, 0), (255, 100, 0), (255, 0, 0)]
        glow_idx = min(3, int((1 - health_ratio) * 3))
        pygame.draw.circle(screen, glow_colors[glow_idx], (x + size // 3, y + size // 3), 2)
        pygame.draw.circle(screen, glow_colors[glow_idx], (x + 2 * size // 3, y + size // 3), 2)
    
    @staticmethod
    def draw_fast_enemy(screen, x, y, size, color=(255, 255, 0)):
        """Fast enemy - sleek bug"""
        # Pointed head
        pygame.draw.polygon(screen, color, [
            (x + size // 2, y),
            (x + size, y + size // 3),
            (x + 3 * size // 4, y + size),
            (x + size // 4, y + size),
            (x, y + size // 3)
        ])
        # Speed lines
        pygame.draw.line(screen, (255, 200, 0), (x - 5, y + size // 3), (x - 10, y + size // 3), 2)
        pygame.draw.line(screen, (255, 200, 0), (x + size + 5, y + size // 3), (x + size + 10, y + size // 3), 2)
        # Eyes
        pygame.draw.circle(screen, (0, 0, 0), (x + size // 3, y + size // 2), 2)
        pygame.draw.circle(screen, (0, 0, 0), (x + 2 * size // 3, y + size // 2), 2)
    
    @staticmethod
    def draw_tanky_enemy(screen, x, y, size, color=(255, 165, 0)):
        """Tanky enemy - armored beast"""
        # Large armored body
        pygame.draw.rect(screen, color, (x, y, size, size))
        # Armor plating
        plate_size = size // 4
        for i in range(2):
            for j in range(2):
                pygame.draw.rect(screen, (200, 100, 0), 
                               (x + i * size // 2, y + j * size // 2, plate_size, plate_size), 2)
        # Spikes
        spike_height = size // 4
        pygame.draw.polygon(screen, (150, 50, 0), [
            (x + size // 4, y - spike_height),
            (x + size // 4 - 4, y),
            (x + size // 4 + 4, y)
        ])
        pygame.draw.polygon(screen, (150, 50, 0), [
            (x + 3 * size // 4, y - spike_height),
            (x + 3 * size // 4 - 4, y),
            (x + 3 * size // 4 + 4, y)
        ])
        # Eyes menacing
        pygame.draw.circle(screen, (255, 0, 0), (x + size // 3, y + size // 2), 3)
        pygame.draw.circle(screen, (255, 0, 0), (x + 2 * size // 3, y + size // 2), 3)
    
    @staticmethod
    def draw_spawner_enemy(screen, x, y, size, color=(200, 50, 200)):
        """Spawner enemy - purple alien that spawns drones"""
        # Body
        pygame.draw.circle(screen, color, (x + size // 2, y + size // 2), size // 2)
        # Energy core
        pygame.draw.circle(screen, (255, 100, 255), (x + size // 2, y + size // 2), size // 4)
        # Spawning tendrils
        for i in range(0, 360, 90):
            import math
            end_x = x + size // 2 + math.cos(math.radians(i)) * (size // 1.5)
            end_y = y + size // 2 + math.sin(math.radians(i)) * (size // 1.5)
            pygame.draw.line(screen, color, (x + size // 2, y + size // 2), (end_x, end_y), 2)
        # Eyes
        pygame.draw.circle(screen, (255, 200, 0), (x + size // 3, y + size // 3), 2)
        pygame.draw.circle(screen, (255, 200, 0), (x + 2 * size // 3, y + size // 3), 2)
    
    @staticmethod
    def draw_drone_enemy(screen, x, y, size, color=(0, 200, 255)):
        """Drone enemy - small cyan fast scout"""
        # Small streamlined body
        pygame.draw.polygon(screen, color, [
            (x + size // 2, y),
            (x + size, y + size // 2),
            (x + size // 2, y + size),
            (x, y + size // 2)
        ])
        # Core
        pygame.draw.circle(screen, (100, 255, 255), (x + size // 2, y + size // 2), size // 4)
        # Propulsion jets
        pygame.draw.rect(screen, (0, 255, 100), (x + size // 4, y + 3 * size // 4, size // 2, size // 4), 1)


class BulletVisual:
    """Enhanced bullet visuals"""
    
    @staticmethod
    def draw_bullet(screen, x, y, width, height, trail_points=None):
        """Draw bullet with trail effect"""
        # Draw trail
        if trail_points and len(trail_points) > 1:
            for i in range(len(trail_points) - 1):
                alpha = int(255 * (i / len(trail_points)))
                trail_color = (150, 200, 255) if i < len(trail_points) // 2 else (100, 150, 255)
                pygame.draw.line(screen, trail_color, trail_points[i], trail_points[i + 1], max(1, width - i // 5))
        
        # Main bullet body
        pygame.draw.rect(screen, (100, 200, 255), (x, y, width, height))
        # Bullet tip glow
        pygame.draw.circle(screen, (200, 255, 255), (int(x + width // 2), int(y - 2)), 2)
        # Outline
        pygame.draw.rect(screen, (150, 220, 255), (x, y, width, height), 1)


class PowerUpVisual:
    """Enhanced power-up visuals with animations"""
    
    @staticmethod
    def draw_health_powerup(screen, x, y, size, pulse=0):
        """Health power-up with pulse effect"""
        pulse_size = size + int(5 * pulse)
        # Outer glow
        pygame.draw.rect(screen, (0, 200, 0), (x - 2, y - 2, size + 4, size + 4), 1)
        # Main square
        pygame.draw.rect(screen, (0, 255, 0), (x, y, size, size))
        # Cross pattern
        pygame.draw.rect(screen, (255, 255, 255), (x + size // 3, y + size // 6, size // 3, 2 * size // 3))
        pygame.draw.rect(screen, (255, 255, 255), (x + size // 6, y + size // 3, 2 * size // 3, size // 3))
        # Pulse border
        pygame.draw.rect(screen, (100, 255, 100), (x - pulse_size // 2, y - pulse_size // 2, size + pulse_size, size + pulse_size), 1)
    
    @staticmethod
    def draw_firerate_powerup(screen, x, y, size, pulse=0):
        """Fire rate power-up with lightning effect"""
        pulse_size = size + int(5 * pulse)
        # Outer glow
        pygame.draw.rect(screen, (255, 255, 0), (x - 2, y - 2, size + 4, size + 4), 1)
        # Main square
        pygame.draw.rect(screen, (255, 255, 0), (x, y, size, size))
        # Lightning bolt pattern
        bolt_points = [
            (x + size // 2, y + size // 4),
            (x + size // 3, y + size // 2),
            (x + 2 * size // 3, y + size // 2),
            (x + size // 2, y + size)
        ]
        pygame.draw.lines(screen, (255, 200, 0), bolt_points, 2)
        # Pulse border
        pygame.draw.rect(screen, (255, 200, 0), (x - pulse_size // 2, y - pulse_size // 2, size + pulse_size, size + pulse_size), 1)

"""
Space-themed graphics for rockets, asteroids, and UFOs
"""
import pygame
import math

class RocketGraphics:
    """Draw different types of rockets/spaceships"""
    
    @staticmethod
    def draw_falcon_rocket(screen, x, y, size, color=(100, 200, 255)):
        """Sleek falcon-style rocket - Knight equivalent"""
        # Main fuselage
        pygame.draw.polygon(screen, color, [
            (x + size // 2, y),
            (x + size // 4, y + size),
            (x + 3 * size // 4, y + size)
        ])
        # Cockpit window
        pygame.draw.circle(screen, (255, 255, 100), (x + size // 2, y + size // 4), size // 6)
        # Engine glow
        pygame.draw.polygon(screen, (255, 100, 0), [
            (x + size // 3, y + size),
            (x + 2 * size // 3, y + size),
            (x + size // 2, y + size + size // 3)
        ])
        # Side fins
        pygame.draw.polygon(screen, (60, 150, 200), [
            (x + size // 4, y + 2 * size // 3),
            (x + size // 8, y + size),
            (x + size // 3, y + 3 * size // 4)
        ])
        pygame.draw.polygon(screen, (60, 150, 200), [
            (x + 3 * size // 4, y + 2 * size // 3),
            (x + 7 * size // 8, y + size),
            (x + 2 * size // 3, y + 3 * size // 4)
        ])
    
    @staticmethod
    def draw_nova_laser(screen, x, y, size, color=(255, 100, 200)):
        """High-tech laser ship - Wizard equivalent"""
        # Main body - angular design
        pygame.draw.polygon(screen, color, [
            (x + size // 2, y),
            (x + size // 4, y + size // 2),
            (x + size // 3, y + size),
            (x + 2 * size // 3, y + size),
            (x + 3 * size // 4, y + size // 2)
        ])
        # Energy core in center
        pygame.draw.circle(screen, (255, 255, 0), (x + size // 2, y + size // 2), size // 5)
        # Energy lines
        for i in range(0, 360, 120):
            end_x = x + size // 2 + math.cos(math.radians(i)) * (size // 3)
            end_y = y + size // 2 + math.sin(math.radians(i)) * (size // 3)
            pygame.draw.line(screen, (200, 200, 0), (x + size // 2, y + size // 2), (end_x, end_y), 2)
    
    @staticmethod
    def draw_shadow_fighter(screen, x, y, size, color=(150, 100, 255)):
        """Sleek fighter jet - Ninja equivalent"""
        # Pointed fuselage
        pygame.draw.polygon(screen, color, [
            (x + size // 2, y),
            (x + size, y + size // 3),
            (x + size // 2, y + size),
            (x, y + size // 3)
        ])
        # Cockpit
        pygame.draw.circle(screen, (255, 200, 0), (x + size // 2, y + size // 3), size // 7)
        # Speed lines effect
        pygame.draw.line(screen, (200, 100, 255), (x + size // 4, y + 2 * size // 3), (x + 3 * size // 4, y + 2 * size // 3), 1)
    
    @staticmethod
    def draw_titan_cruiser(screen, x, y, size, color=(0, 200, 100)):
        """Heavy armored cruiser - Robot equivalent"""
        # Large hexagonal body
        angles = [i * 60 for i in range(6)]
        points = []
        for angle in angles:
            px = x + size // 2 + math.cos(math.radians(angle)) * (size // 2)
            py = y + size // 2 + math.sin(math.radians(angle)) * (size // 2)
            points.append((px, py))
        pygame.draw.polygon(screen, color, points)
        # Inner shield
        pygame.draw.circle(screen, (0, 255, 150), (x + size // 2, y + size // 2), size // 3, 2)
        # Energy nodes at corners
        for i in range(0, 360, 120):
            node_x = x + size // 2 + math.cos(math.radians(i)) * (size // 3)
            node_y = y + size // 2 + math.sin(math.radians(i)) * (size // 3)
            pygame.draw.circle(screen, (0, 255, 100), (node_x, node_y), size // 8)
    
    @staticmethod
    def draw_phoenix_explorer(screen, x, y, size, color=(255, 100, 50)):
        """Phoenix-inspired explorer craft with wings - revive ability"""
        # Main body
        pygame.draw.ellipse(screen, color, (x + size // 4, y + size // 4, size // 2, size // 2))
        # Phoenix wings (folded)
        pygame.draw.polygon(screen, (255, 50, 0), [
            (x + size // 4, y + size // 3),
            (x, y + size // 2),
            (x + size // 3, y + size // 2)
        ])
        pygame.draw.polygon(screen, (255, 50, 0), [
            (x + 3 * size // 4, y + size // 3),
            (x + size, y + size // 2),
            (x + 2 * size // 3, y + size // 2)
        ])
        # Tail flame
        pygame.draw.polygon(screen, (255, 150, 0), [
            (x + 2 * size // 5, y + 3 * size // 4),
            (x + 3 * size // 5, y + 3 * size // 4),
            (x + size // 2, y + size)
        ])
    
    @staticmethod
    def draw_mini_phoenix(screen, x, y, size, color=(255, 100, 50)):
        """Smaller phoenix scout - spawned from main phoenix on revive"""
        # Similar to phoenix_explorer but smaller and more streamlined
        pygame.draw.ellipse(screen, color, (x + size // 3, y + size // 3, size // 3, size // 3))
        # Mini wings
        pygame.draw.polygon(screen, (255, 80, 0), [
            (x + size // 3, y + size // 2),
            (x - size // 4, y + size // 2),
            (x + size // 5, y + size // 2 + size // 4)
        ])
        pygame.draw.polygon(screen, (255, 80, 0), [
            (x + 2 * size // 3, y + size // 2),
            (x + size + size // 4, y + size // 2),
            (x + 4 * size // 5, y + size // 2 + size // 4)
        ])


class AsteroidGraphics:
    """Draw asteroids of various sizes"""
    
    @staticmethod
    def draw_small_asteroid(screen, x, y, size, color=(150, 100, 50)):
        """Small asteroid (1-2 hits)"""
        # Jagged rock shape
        points = [
            (x + size // 2, y),
            (x + size, y + size // 4),
            (x + 5 * size // 6, y + size),
            (x + size // 3, y + 5 * size // 6),
            (x, y + size // 2),
            (x + size // 4, y + size // 4)
        ]
        pygame.draw.polygon(screen, color, points)
        # Crater details
        pygame.draw.circle(screen, (100, 70, 30), (x + size // 3, y + size // 3), size // 6)
        pygame.draw.circle(screen, (100, 70, 30), (x + 2 * size // 3, y + 2 * size // 3), size // 8)
    
    @staticmethod
    def draw_medium_asteroid(screen, x, y, size, color=(180, 120, 60)):
        """Medium asteroid (2-3 hits)"""
        # Larger jagged rock
        points = [
            (x + size // 2, y),
            (x + size, y + size // 3),
            (x + 4 * size // 5, y + size),
            (x + size // 2, y + 5 * size // 6),
            (x + size // 5, y + size),
            (x, y + size // 2),
            (x + size // 6, y + size // 3)
        ]
        pygame.draw.polygon(screen, color, points)
        # Crater details
        pygame.draw.circle(screen, (120, 80, 40), (x + 2 * size // 5, y + 2 * size // 5), size // 5)
        pygame.draw.circle(screen, (120, 80, 40), (x + 3 * size // 5, y + 3 * size // 5), size // 6)
        pygame.draw.circle(screen, (120, 80, 40), (x + size // 3, y + 2 * size // 3), size // 7)
    
    @staticmethod
    def draw_large_asteroid(screen, x, y, size, color=(200, 140, 70)):
        """Large asteroid (3+ hits)"""
        # Very jagged massive rock
        points = [
            (x + size // 2, y),
            (x + size, y + size // 4),
            (x + 5 * size // 6, y + size // 2),
            (x + size, y + 3 * size // 4),
            (x + 2 * size // 3, y + size),
            (x + size // 3, y + 5 * size // 6),
            (x + size // 6, y + size),
            (x, y + 2 * size // 3),
            (x + size // 6, y + size // 3),
            (x, y + size // 4)
        ]
        pygame.draw.polygon(screen, color, points)
        # Multiple crater details
        pygame.draw.circle(screen, (140, 90, 50), (x + 2 * size // 5, y + 2 * size // 5), size // 4)
        pygame.draw.circle(screen, (140, 90, 50), (x + 3 * size // 5, y + size // 3), size // 5)
        pygame.draw.circle(screen, (140, 90, 50), (x + size // 2, y + 3 * size // 5), size // 6)
        pygame.draw.circle(screen, (140, 90, 50), (x + size // 4, y + 3 * size // 4), size // 7)


class UFOGraphics:
    """Draw UFO enemies with different sizes"""
    
    @staticmethod
    def draw_scout_ufo(screen, x, y, size, color=(150, 100, 255)):
        """Small scout UFO - classic flying saucer"""
        # Main saucer body (larger ellipse)
        pygame.draw.ellipse(screen, color, (x + size // 8, y + size // 4, 3 * size // 4, size // 3))
        # Top dome (bulge on top)
        pygame.draw.arc(screen, (200, 150, 255), (x + size // 4, y - size // 8, size // 2, size // 2), 0, 3.14159, 3)
        # Center window/dome
        pygame.draw.circle(screen, (255, 200, 255), (x + size // 2, y + size // 3), size // 6)
        # Window glow
        pygame.draw.circle(screen, (100, 255, 200), (x + size // 2, y + size // 3), size // 8, 2)
        # Landing legs (3 pods)
        leg_positions = [size // 3, size // 2, 2 * size // 3]
        for leg_x in leg_positions:
            # Leg line
            pygame.draw.line(screen, color, (x + leg_x, y + size // 2 + size // 3), (x + leg_x, y + size), 2)
            # Landing foot
            pygame.draw.circle(screen, (200, 150, 255), (x + leg_x, y + size), size // 10)
        # Hull details
        pygame.draw.ellipse(screen, color, (x + size // 8, y + size // 4, 3 * size // 4, size // 3), 2)
    
    @staticmethod
    def draw_capital_ufo(screen, x, y, size, color=(200, 50, 255)):
        """Large capital UFO - mothership"""
        # Main hull - larger saucer
        pygame.draw.ellipse(screen, color, (x + size // 10, y + size // 5, 4 * size // 5, size // 3))
        # Hull outline
        pygame.draw.ellipse(screen, (255, 150, 255), (x + size // 10, y + size // 5, 4 * size // 5, size // 3), 3)
        # Tall center tower/dome
        pygame.draw.rect(screen, color, (x + size // 2 - size // 8, y - size // 4, size // 4, size // 2))
        pygame.draw.ellipse(screen, (255, 100, 255), (x + size // 2 - size // 6, y - size // 5, size // 3, size // 6))
        # Main observation dome
        pygame.draw.circle(screen, (255, 200, 255), (x + size // 2, y + size // 4), size // 5)
        pygame.draw.circle(screen, (100, 255, 200), (x + size // 2, y + size // 4), size // 7, 3)
        # Landing pods (4 legs for mothership)
        leg_positions = [size // 5, 2 * size // 5, 3 * size // 5, 4 * size // 5]
        for leg_x in leg_positions:
            # Reinforced legs
            pygame.draw.line(screen, color, (x + leg_x, y + size // 2 + size // 6), (x + leg_x, y + size), 3)
            # Double feet
            pygame.draw.circle(screen, (255, 150, 255), (x + leg_x - size // 12, y + size), size // 8)
            pygame.draw.circle(screen, (255, 150, 255), (x + leg_x + size // 12, y + size), size // 8)
        # Energy beams underneath
        pygame.draw.line(screen, (150, 255, 200), (x + size // 3, y + size // 2 + size // 4), (x + size // 3, y + size + size // 4), 2)
        pygame.draw.line(screen, (150, 255, 200), (x + 2 * size // 3, y + size // 2 + size // 4), (x + 2 * size // 3, y + size + size // 4), 2)


class ProjectileGraphics:
    """Draw space-themed projectiles"""
    
    @staticmethod
    def draw_laser(screen, x, y, width, height, color=(0, 255, 100)):
        """Energy laser shot"""
        # Main laser beam
        pygame.draw.rect(screen, color, (x, y, width, height))
        # Glow effect
        pygame.draw.line(screen, (100, 255, 150), (x, y), (x, y + height), 3)
        # Tip glow
        pygame.draw.circle(screen, (150, 255, 200), (x + width // 2, y - 3), 2)


class PowerUpGraphics:
    """Draw space-themed power-ups"""
    
    @staticmethod
    def draw_shield_core(screen, x, y, size):
        """Shield power-up - defensive core"""
        pygame.draw.circle(screen, (0, 150, 255), (x + size // 2, y + size // 2), size // 2)
        pygame.draw.circle(screen, (0, 200, 255), (x + size // 2, y + size // 2), size // 2 - 3, 3)
        # Inner core
        pygame.draw.circle(screen, (100, 255, 255), (x + size // 2, y + size // 2), size // 4)
    
    @staticmethod
    def draw_boost_core(screen, x, y, size):
        """Fire rate boost - energy pulse"""
        pygame.draw.circle(screen, (255, 200, 0), (x + size // 2, y + size // 2), size // 2)
        # Star pattern
        for i in range(0, 360, 90):
            end_x = x + size // 2 + math.cos(math.radians(i)) * (size // 2 + 3)
            end_y = y + size // 2 + math.sin(math.radians(i)) * (size // 2 + 3)
            pygame.draw.line(screen, (255, 255, 0), (x + size // 2, y + size // 2), (end_x, end_y), 2)

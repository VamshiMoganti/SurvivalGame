"""
Advanced visual effects for enhanced gameplay experience
"""
import pygame
import math
import random


class NeonGlow:
    """Draw glowing neon effects around objects"""
    @staticmethod
    def draw_neon_circle(screen, x, y, radius, color, intensity=2):
        """Draw neon-style glowing circle"""
        # Multiple rings for glow effect
        for i in range(intensity, 0, -1):
            alpha_color = tuple(min(int(c * (intensity - i) / intensity * 0.5), 255) for c in color)
            pygame.draw.circle(screen, alpha_color, (int(x), int(y)), radius + i * 3, 2)
        # Core bright circle
        pygame.draw.circle(screen, color, (int(x), int(y)), radius, 2)

    @staticmethod
    def draw_neon_rect(screen, rect, color, width=2):
        """Draw neon-style glowing rectangle"""
        # Outer glow
        glow_color = tuple(min(int(c * 0.3), 255) for c in color)
        for i in range(1, 4):
            pygame.draw.rect(screen, glow_color, rect.inflate(i * 2, i * 2), 1)
        # Main rectangle
        pygame.draw.rect(screen, color, rect, width)


class ParticleTrail:
    """Create particle trails for bullets and effects"""
    def __init__(self, x, y, color=(100, 200, 255), lifetime=10, size=3):
        self.x = x
        self.y = y
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = size
        self.alpha = 255

    def update(self):
        self.lifetime -= 1
        self.alpha = int(255 * (self.lifetime / self.max_lifetime))

    def draw(self, screen):
        # Fading trail particle
        fade_color = tuple(int(c * (self.lifetime / self.max_lifetime)) for c in self.color)
        pygame.draw.circle(screen, fade_color, (int(self.x), int(self.y)), max(1, int(self.size * (self.lifetime / self.max_lifetime))))

    def is_alive(self):
        return self.lifetime > 0


class Nebula:
    """Animated nebula cloud effect for background"""
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.opacity = 0.1
        self.drift_x = random.uniform(-0.5, 0.5)
        self.drift_y = random.uniform(-0.3, 0.3)
        self.pulse = 0

    def update(self):
        self.x += self.drift_x
        self.y += self.drift_y
        self.pulse = (self.pulse + 0.02) % (2 * math.pi)
        # Pulse opacity
        self.opacity = 0.1 + 0.05 * math.sin(self.pulse)

    def draw(self, screen):
        # Create nebula surface and draw it with transparency
        try:
            nebula_surface = pygame.Surface((self.width, self.height))
            nebula_surface.fill((0, 0, 0))
            nebula_surface.set_colorkey((0, 0, 0))
            
            # Draw gradient nebula using circles
            center_x = self.width // 2
            center_y = self.height // 2
            for i in range(5, 0, -1):
                radius = (self.width // 2) * (i / 5)
                fade_color = tuple(int(c * (6 - i) / 5 * self.opacity) for c in self.color)
                pygame.draw.circle(nebula_surface, fade_color, (int(center_x), int(center_y)), int(radius))
            
            nebula_surface.set_alpha(int(255 * self.opacity))
            screen.blit(nebula_surface, (int(self.x), int(self.y)))
        except:
            pass


class EnergyPulse:
    """Expanding energy wave effect"""
    def __init__(self, x, y, max_radius, color=(100, 255, 200), duration=30):
        self.x = x
        self.y = y
        self.max_radius = max_radius
        self.color = color
        self.duration = duration
        self.elapsed = 0

    def update(self):
        self.elapsed += 1

    def draw(self, screen):
        if self.elapsed < self.duration:
            progress = self.elapsed / self.duration
            radius = int(self.max_radius * progress)
            alpha = int(255 * (1 - progress))
            
            # Draw expanding ring
            color_with_alpha = tuple(c for c in self.color)
            try:
                # Draw multiple rings for effect
                for width in range(2, 0, -1):
                    ring_color = tuple(int(c * (1 - progress) * 0.7) for c in self.color)
                    pygame.draw.circle(screen, ring_color, (int(self.x), int(self.y)), radius, width)
            except:
                pass

    def is_done(self):
        return self.elapsed >= self.duration


class ScreenFlash:
    """Screen flash effect for big events"""
    def __init__(self, color=(255, 255, 255), duration=20):
        self.color = color
        self.duration = duration
        self.elapsed = 0

    def update(self):
        self.elapsed += 1

    def draw(self, screen):
        if self.elapsed < self.duration:
            alpha = int(255 * (1 - self.elapsed / self.duration))
            flash_surface = pygame.Surface(screen.get_size())
            flash_surface.fill(self.color)
            flash_surface.set_alpha(alpha)
            screen.blit(flash_surface, (0, 0))

    def is_done(self):
        return self.elapsed >= self.duration


class ComboMeterVisual:
    """Enhanced visual for combo meter"""
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.combo = 0
        self.max_combo = 0
        self.pulse = 0

    def update(self, combo):
        self.combo = combo
        self.pulse = (self.pulse + 0.05) % (2 * math.pi)

    def draw(self, screen):
        if self.combo > 0:
            # Animated combo meter
            bar_width = 300
            bar_height = 30
            bar_x = self.screen_width // 2 - bar_width // 2
            bar_y = self.screen_height - 90

            # Pulse glow
            glow_intensity = int(10 + 5 * math.sin(self.pulse))
            glow_color = (255, 215, 0)
            for i in range(glow_intensity, 0, -2):
                glow = tuple(int(c * 0.3) for c in glow_color)
                pygame.draw.rect(screen, glow, (bar_x - i, bar_y - i, bar_width + i * 2, bar_height + i * 2), 1)

            # Main meter
            pygame.draw.rect(screen, (60, 60, 0), (bar_x, bar_y, bar_width, bar_height), 0)
            
            combo_mult = 1.0 + (self.combo // 3) * 0.2
            fill_width = min(bar_width, int(bar_width * (self.combo / 50)))
            pygame.draw.rect(screen, (255, 215, 0), (bar_x, bar_y, fill_width, bar_height))
            pygame.draw.rect(screen, glow_color, (bar_x, bar_y, bar_width, bar_height), 3)

            # Text
            font = pygame.font.SysFont(None, 28)
            text = font.render(f"x{combo_mult:.1f} COMBO!", True, (255, 215, 0))
            screen.blit(text, (bar_x + 80, bar_y + 2))


class LensFlare:
    """Lens flare effect near center"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lifetime = 30
        self.max_lifetime = 30

    def update(self):
        self.lifetime -= 1

    def draw(self, screen):
        if self.lifetime > 0:
            progress = 1 - (self.lifetime / self.max_lifetime)
            
            # Central glow
            size = int(10 + progress * 30)
            alpha = int(100 * (1 - progress))
            glow_color = (200, 200, 100)
            
            # Draw lens flare elements
            for i in range(3):
                offset = int(20 + progress * 60)
                angle = (i * 120) * math.pi / 180
                flare_x = self.x + math.cos(angle) * offset
                flare_y = self.y + math.sin(angle) * offset
                pygame.draw.circle(screen, glow_color, (int(flare_x), int(flare_y)), max(1, size // (i + 1)))

    def is_done(self):
        return self.lifetime <= 0


class ShieldEffect:
    """Visual shield generator effect"""
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.rotation = 0
        self.lifetime = 1000  # Long effect

    def update(self):
        self.rotation = (self.rotation + 3) % 360

    def draw(self, screen):
        # Rotating hexagon shield
        angles = [i * 60 + self.rotation for i in range(6)]
        points = []
        for angle in angles:
            px = self.x + math.cos(math.radians(angle)) * self.radius
            py = self.y + math.sin(math.radians(angle)) * self.radius
            points.append((px, py))
        
        # Draw shield outline with glow
        shield_color = (0, 255, 150)
        for i in range(2, 0, -1):
            pygame.draw.polygon(screen, tuple(min(int(c * 0.4), 255) for c in shield_color), points, i + 1)
        pygame.draw.polygon(screen, shield_color, points, 2)

    def is_done(self):
        return False


class ScreenTransition:
    """Fade transition effects"""
    def __init__(self, direction='fade_out', duration=30, color=(0, 0, 0)):
        self.direction = direction  # fade_in, fade_out, wipe_left, wipe_right
        self.duration = duration
        self.elapsed = 0
        self.color = color

    def update(self):
        self.elapsed += 1

    def draw(self, screen, width, height):
        if self.elapsed >= self.duration:
            return False
        
        progress = self.elapsed / self.duration
        
        if self.direction == 'fade_out':
            alpha = int(255 * progress)
        elif self.direction == 'fade_in':
            alpha = int(255 * (1 - progress))
        else:
            alpha = 200

        transition_surface = pygame.Surface((width, height))
        transition_surface.fill(self.color)
        
        if 'wipe' in self.direction:
            if 'left' in self.direction:
                wipe_width = int(width * progress)
                transition_surface = pygame.Surface((wipe_width, height))
                transition_surface.fill(self.color)
                screen.blit(transition_surface, (0, 0))
                return True
        
        transition_surface.set_alpha(alpha)
        screen.blit(transition_surface, (0, 0))
        return True

    def is_done(self):
        return self.elapsed >= self.duration


class GlitchEffect:
    """Digital glitch effect (rare, for special moments)"""
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.lifetime = 15
        self.max_lifetime = 15

    def update(self):
        self.lifetime -= 1

    def draw(self, screen):
        if self.lifetime > 0:
            # Random horizontal displacement lines
            for _ in range(random.randint(3, 8)):
                line_y = random.randint(int(self.y), int(self.y + self.height))
                offset = random.randint(-10, 10)
                color = random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255)])
                pygame.draw.line(screen, color, (int(self.x + offset), line_y), 
                                (int(self.x + self.width + offset), line_y), 2)

    def is_done(self):
        return self.lifetime <= 0

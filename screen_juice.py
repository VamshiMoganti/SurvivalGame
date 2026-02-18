"""
Visual Juice System - Advanced screen effects, animations, and visual polish
Makes the game feel MUCH more responsive and satisfying
"""
import pygame
import math
import random


class ScreenJuice:
    """Advanced screen effects for satisfying feedback"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen_shake = 0
        self.screen_tilt = 0
        self.chromatic_aberration = 0
        self.vignette_strength = 0
        self.scanline_intensity = 0
        self.bloom_intensity = 0
    
    def trigger_shake(self, intensity=5, duration=10):
        """Trigger screen shake with proper intensity"""
        self.screen_shake = max(self.screen_shake, intensity)
    
    def trigger_tilt(self, angle=3):
        """Tilt screen slightly"""
        self.screen_tilt = angle
    
    def add_chromatic_aberration(self, amount=5):
        """Add RGB channel separation"""
        self.chromatic_aberration = max(self.chromatic_aberration, amount)
    
    def update(self):
        """Update all juice effects"""
        if self.screen_shake > 0:
            self.screen_shake *= 0.9  # Decay shake
        if self.chromatic_aberration > 0:
            self.chromatic_aberration *= 0.95
        if self.vignette_strength < 0.1:
            self.vignette_strength = 0
    
    def get_shake_offset(self):
        """Get random shake offset"""
        if self.screen_shake > 0:
            return (
                random.randint(int(-self.screen_shake), int(self.screen_shake)),
                random.randint(int(-self.screen_shake), int(self.screen_shake))
            )
        return (0, 0)
    
    def draw_vignette(self, screen):
        """Draw dark vignette around edges"""
        vignette = pygame.Surface((self.width, self.height))
        vignette.fill((0, 0, 0))
        
        # Radial gradient vignette
        center_x, center_y = self.width // 2, self.height // 2
        max_dist = math.sqrt(center_x**2 + center_y**2)
        
        for x in range(self.width):
            for y in range(self.height):
                dx = x - center_x
                dy = y - center_y
                dist = math.sqrt(dx**2 + dy**2)
                alpha = int(200 * (dist / max_dist) * 0.3)  # Subtle
                
                if alpha > 0:
                    pygame.draw.circle(vignette, (0, 0, 0), (x, y), 1)
        
        vignette.set_alpha(int(100 * 0.2))  # Very subtle
        screen.blit(vignette, (0, 0))
    
    def draw_scanlines(self, screen):
        """Draw subtle scanline effect"""
        if self.scanline_intensity > 0:
            scanlines = pygame.Surface((self.width, self.height))
            scanlines.fill((255, 255, 255))
            
            for y in range(0, self.height, 2):
                pygame.draw.line(scanlines, (0, 0, 0), (0, y), (self.width, y), 1)
            
            scanlines.set_alpha(int(30 * self.scanline_intensity))
            screen.blit(scanlines, (0, 0))


class ParticleExplosion:
    """Enhanced explosion with many particle types"""
    
    def __init__(self, x, y, color=(255, 165, 0), particle_count=30, particle_types='mixed'):
        self.x = x
        self.y = y
        self.particles = []
        self.particle_types = particle_types
        
        for _ in range(particle_count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            p_type = random.choice(['spark', 'smoke', 'debris']) if particle_types == 'mixed' else particle_types
            lifetime = random.randint(20, 50)
            
            self.particles.append({
                'x': x,
                'y': y,
                'vx': vx,
                'vy': vy,
                'lifetime': lifetime,
                'max_lifetime': lifetime,
                'type': p_type,
                'color': color,
                'size': random.randint(3, 8),
                'rotation': random.uniform(0, 360)
            })
    
    def update(self):
        for p in self.particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.3  # Gravity
            p['lifetime'] -= 1
            p['rotation'] += random.uniform(-10, 10)
            
            if p['lifetime'] <= 0:
                self.particles.remove(p)
    
    def draw(self, screen):
        for p in self.particles:
            alpha = p['lifetime'] / p['max_lifetime']
            size = int(p['size'] * alpha)
            
            if p['type'] == 'spark':
                # Bright sparks
                color = tuple(int(c * alpha) for c in p['color'])
                pygame.draw.circle(screen, color, (int(p['x']), int(p['y'])), max(1, size))
            elif p['type'] == 'smoke':
                # Fading smoke
                smoke_color = tuple(int(c * alpha * 0.5) for c in (100, 100, 100))
                pygame.draw.circle(screen, smoke_color, (int(p['x']), int(p['y'])), max(3, size))
            elif p['type'] == 'debris':
                # Square debris
                color = tuple(int(c * alpha * 0.8) for c in p['color'])
                rect = pygame.Rect(int(p['x']) - size // 2, int(p['y']) - size // 2, size, size)
                pygame.draw.rect(screen, color, rect)
    
    def is_done(self):
        return len(self.particles) == 0


class FloatingNumber:
    """Animated floating numbers with lerp movement"""
    
    def __init__(self, x, y, text, color=(255, 255, 0), lifetime=60, target_y_offset=50):
        self.x = x
        self.y = y
        self.target_y = y - target_y_offset
        self.start_x = x
        self.start_y = y
        self.text = text
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = 28
        self.start_size = 28
    
    def update(self):
        progress = 1 - (self.lifetime / self.max_lifetime)
        
        # Smooth easing (ease out)
        ease = 1 - (1 - progress) ** 2
        
        self.x = self.start_x + (0) * ease
        self.y = self.start_y + (self.target_y - self.start_y) * ease
        self.size = int(self.start_size * (1 + progress * 0.3))  # Grow slightly
        self.lifetime -= 1
    
    def draw(self, screen, font):
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        color = tuple(int(c * (self.lifetime / self.max_lifetime)) for c in self.color)
        
        text_surface = font.render(self.text, True, color)
        text_surface.set_alpha(alpha)
        screen.blit(text_surface, (int(self.x) - 20, int(self.y) - 10))
    
    def is_alive(self):
        return self.lifetime > 0


class GlowingElement:
    """UI element with pulsing glow"""
    
    def __init__(self, x, y, width, height, color=(0, 255, 255), pulse_speed=0.05):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.pulse_val = 0
        self.pulse_speed = pulse_speed
    
    def update(self):
        self.pulse_val = (self.pulse_val + self.pulse_speed) % (2 * math.pi)
    
    def draw(self, screen):
        # Pulsing glow intensity
        glow_intensity = 2 + int(3 * math.sin(self.pulse_val))
        
        # Draw glow rings
        for i in range(glow_intensity, 0, -1):
            glow_color = tuple(min(int(c * (glow_intensity - i) / glow_intensity * 0.4), 255) for c in self.color)
            pygame.draw.rect(screen, glow_color, 
                           (self.x - i * 2, self.y - i * 2, self.width + i * 4, self.height + i * 4), 1)
        
        # Draw main element
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 2)


class MotionTrail:
    """Motion trail effect for moving objects"""
    
    def __init__(self, x, y, color=(100, 200, 255), max_length=15):
        self.positions = [(x, y)]
        self.color = color
        self.max_length = max_length
        self.lifetimes = [20]
    
    def add_position(self, x, y):
        self.positions.append((x, y))
        self.lifetimes.append(20)
        
        if len(self.positions) > self.max_length:
            self.positions.pop(0)
            self.lifetimes.pop(0)
    
    def update(self):
        for i in range(len(self.lifetimes)):
            self.lifetimes[i] -= 1
    
    def draw(self, screen):
        for i, (x, y) in enumerate(self.positions):
            alpha = self.lifetimes[i] / 20 if i < len(self.lifetimes) else 0
            trail_color = tuple(int(c * alpha) for c in self.color)
            size = max(1, int(5 * alpha))
            pygame.draw.circle(screen, trail_color, (int(x), int(y)), size)


class ComboVisualizer:
    """Advanced combo system visualization"""
    
    def __init__(self, screen_width, screen_height):
        self.width = screen_width
        self.height = screen_height
        self.combo = 0
        self.combo_flash = 0
        self.milestone_flash = 0
        self.milestones_reached = set()
    
    def update(self, combo):
        self.combo = combo
        
        # Check for milestones (every 10 combos)
        if combo > 0 and combo % 10 == 0 and combo not in self.milestones_reached:
            self.milestone_flash = 40
            self.milestones_reached.add(combo)
        
        if self.combo_flash > 0:
            self.combo_flash -= 1
        if self.milestone_flash > 0:
            self.milestone_flash -= 1
    
    def draw_advanced_meter(self, screen, font_small, font_large):
        if self.combo > 0:
            bar_width = 350
            bar_height = 40
            bar_x = self.width // 2 - bar_width // 2
            bar_y = self.height - 100
            
            # Milestone effect
            milestone_pulse = 0
            if self.milestone_flash > 0:
                milestone_pulse = int(10 * math.sin((40 - self.milestone_flash) / 40 * math.pi))
            
            # Animated border glow
            glow_rings = 3
            combo_mult = 1.0 + (self.combo // 3) * 0.2
            
            # Color based on combo (rainbow effect)
            combo_ratio = min(self.combo / 50, 1.0)
            r = int(255 * combo_ratio)
            g = int(255 * (1 - abs(combo_ratio - 0.5) * 2))
            b = int(255 * (1 - combo_ratio))
            combo_color = (r, g, b)
            
            # Draw glowing border with rainbow color
            for i in range(glow_rings + milestone_pulse // 2, 0, -1):
                glow_color = tuple(min(int(c * (glow_rings - i) / glow_rings * 0.6), 255) for c in combo_color)
                pygame.draw.rect(screen, glow_color, 
                               (bar_x - i * 2, bar_y - i * 2 - milestone_pulse // 2, 
                                bar_width + i * 4, bar_height + i * 4), 2)
            
            # Background
            pygame.draw.rect(screen, (20, 20, 40), (bar_x, bar_y, bar_width, bar_height))
            
            # Fill bar
            fill_width = min(bar_width, int(bar_width * (self.combo / 50)))
            pygame.draw.rect(screen, combo_color, (bar_x, bar_y, fill_width, bar_height))
            
            # Border
            pygame.draw.rect(screen, combo_color, (bar_x, bar_y, bar_width, bar_height), 3)
            
            # Combo text with glow
            combo_text = f"x{combo_mult:.1f} COMBO!"
            text_surface = font_large.render(combo_text, True, combo_color)
            text_glow = font_large.render(combo_text, True, tuple(min(int(c * 0.5), 255) for c in combo_color))
            
            screen.blit(text_glow, (bar_x + 50 + 2, bar_y + 5 + 2))
            screen.blit(text_surface, (bar_x + 50, bar_y + 5))
            
            # Milestone indicator
            if self.milestone_flash > 0:
                mile_text = f"MILESTONE x{self.combo}!"
                mile_surface = font_small.render(mile_text, True, (255, 215, 0))
                screen.blit(mile_surface, (bar_x + 20, bar_y - 40))


class ShinyNumber:
    """Number that appears with shine effect"""
    
    def __init__(self, x, y, value, color=(255, 215, 0)):
        self.x = x
        self.y = y
        self.value = value
        self.color = color
        self.lifetime = 40
        self.max_lifetime = 40
        self.shine_pos = 0
    
    def update(self):
        self.lifetime -= 1
        self.shine_pos = (self.shine_pos + 5) % 360
    
    def draw(self, screen, font):
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        
        # Draw number with shine
        text = f"+{self.value}"
        text_surface = font.render(text, True, self.color)
        text_surface.set_alpha(alpha)
        
        # Shift position upward as it fades
        offset_y = int((self.max_lifetime - self.lifetime) * 1.5)
        screen.blit(text_surface, (int(self.x), int(self.y) - offset_y))
    
    def is_alive(self):
        return self.lifetime > 0


class PulsingBar:
    """Health/Shield bar with pulsing effect"""
    
    def __init__(self, x, y, width, height, color=(0, 255, 0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.pulse_val = 0
        self.fill_amount = 1.0
        self.danger_level = 0  # 0-1, for pulsing speed
    
    def update(self, fill_amount, danger_level=0):
        self.fill_amount = fill_amount
        self.danger_level = danger_level
        pulse_speed = 0.05 + (danger_level * 0.1)
        self.pulse_val = (self.pulse_val + pulse_speed) % (2 * math.pi)
    
    def draw(self, screen):
        # Background
        pygame.draw.rect(screen, (30, 30, 30), (self.x, self.y, self.width, self.height))
        
        # Pulsing fill
        fill_width = int(self.width * max(0, self.fill_amount))
        
        # Add pulse effect based on danger
        pulse_effect = int(3 * self.danger_level * math.sin(self.pulse_val))
        pygame.draw.rect(screen, self.color, 
                        (self.x, self.y + pulse_effect // 2, fill_width, self.height - pulse_effect))
        
        # Shimmer effect on the edge
        if fill_width > 0:
            shimmer_x = int(self.x + fill_width - 3)
            pygame.draw.rect(screen, tuple(min(int(c * 1.3), 255) for c in self.color),
                            (shimmer_x, self.y, 3, self.height))
        
        # Border
        border_color = self.color if self.danger_level < 0.5 else (255, int(100 * (1 - self.danger_level)), 0)
        pygame.draw.rect(screen, border_color, (self.x, self.y, self.width, self.height), 2)


class StarburstEffect:
    """Starburst explosion effect (like a hit marker)"""
    
    def __init__(self, x, y, color=(255, 255, 255), size=30):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.lifetime = 20
        self.max_lifetime = 20
    
    def update(self):
        self.lifetime -= 1
    
    def draw(self, screen):
        progress = 1 - (self.lifetime / self.max_lifetime)
        alpha = int(255 * (1 - progress))
        
        radius = int(self.size * progress)
        ray_length = int(self.size * 2 * progress)
        
        # Draw radiating rays
        for i in range(8):
            angle = (i / 8) * 2 * math.pi
            end_x = self.x + math.cos(angle) * ray_length
            end_y = self.y + math.sin(angle) * ray_length
            
            ray_color = tuple(int(c * (1 - progress)) for c in self.color)
            pygame.draw.line(screen, ray_color, (self.x, self.y), (end_x, end_y), 2)
        
        # Center circle
        center_color = self.color
        pygame.draw.circle(screen, center_color, (int(self.x), int(self.y)), max(2, radius))
    
    def is_done(self):
        return self.lifetime <= 0


class RainbowText:
    """Text that cycles through rainbow colors"""
    
    def __init__(self, x, y, text, lifetime=60):
        self.x = x
        self.y = y
        self.text = text
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.hue = 0
    
    def update(self):
        self.hue = (self.hue + 5) % 360
        self.lifetime -= 1
    
    def draw(self, screen, font):
        # Convert HSV to RGB
        import colorsys
        rgb = colorsys.hsv_to_rgb(self.hue / 360, 0.8, 1.0)
        color = tuple(int(c * 255) for c in rgb)
        
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        text_surface = font.render(self.text, True, color)
        text_surface.set_alpha(alpha)
        
        screen.blit(text_surface, (int(self.x), int(self.y)))
    
    def is_alive(self):
        return self.lifetime > 0

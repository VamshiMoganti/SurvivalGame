"""
🎮 ENHANCED BOSS SYSTEM - Strategy & Challenge
Each boss is unique with special abilities and personality
"""

import pygame
import random
import math

class EnhancedBoss:
    """
    Advanced boss with health, special abilities, and personality
    """
    
    def __init__(self, x, y, wave, boss_type='destroyer', base_difficulty=1.0):
        self.x = x
        self.y = y
        self.wave = wave
        self.boss_type = boss_type
        
        # Import story data for boss stats
        from story import BOSS_TYPES, get_boss_health
        
        self.boss_data = BOSS_TYPES.get(boss_type, BOSS_TYPES['destroyer'])
        self.max_health = get_boss_health(wave, base_difficulty)
        self.health = self.max_health
        
        self.size = 60
        self.speed = 1.5 + (wave * 0.15)  # Speed scales with wave
        self.direction = random.choice([-1, 1])
        
        # Special abilities based on type
        self.abilities = self._init_abilities()
        self.attack_timer = 0
        self.attack_delay = 30
        self.is_attacking = False
        self.attack_particles = []
        
        # Visual properties
        self.color = self.boss_data['color']
        self.glow_intensity = 0
        self.rotation = 0
        self.health_bar_display = 1.0
    
    def _init_abilities(self):
        """Initialize special abilities based on boss type"""
        abilities = []
        
        if self.boss_type == 'destroyer':
            abilities = ['rapid_fire', 'shield_pulse']
        elif self.boss_type == 'interceptor':
            abilities = ['dodge_pattern', 'speed_burst']
        elif self.boss_type == 'commander':
            abilities = ['summon_drones', 'shield_pulse', 'rapid_fire']
        elif self.boss_type == 'apex':
            abilities = ['berserk_mode', 'phase_shift', 'rapid_fire']
        elif self.boss_type == 'mothership':
            abilities = ['core_blast', 'shield_grid', 'summon_squadrons', 'berserk_mode']
        
        return abilities
    
    def update(self):
        """Update boss position and abilities"""
        # Horizontal movement
        self.x += self.speed * self.direction
        if self.x < 100 or self.x > 1000 - 100:
            self.direction *= -1
        
        # Slow vertical drift downward
        self.y += 0.3
        
        # Update animation
        self.rotation += 2
        self.glow_intensity = 100 + 50 * math.sin(self.rotation / 30)
        
        # Update health display smoother
        target_display = max(0, self.health / max(1, self.max_health))
        self.health_bar_display = self.health_bar_display * 0.9 + target_display * 0.1
        
        # Update ability timer
        self.attack_timer += 1
        
        # Update attack particles
        for particle in self.attack_particles[:]:
            particle['lifetime'] -= 1
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            if particle['lifetime'] <= 0:
                self.attack_particles.remove(particle)
    
    def take_damage(self, damage):
        """Boss takes damage"""
        self.health -= damage
        
        # Add hit effect
        for _ in range(5):
            self.attack_particles.append({
                'x': self.x + random.randint(-30, 30),
                'y': self.y + random.randint(-30, 30),
                'vx': random.uniform(-3, 3),
                'vy': random.uniform(-5, -1),
                'lifetime': 20,
                'size': random.randint(2, 5),
                'color': (255, 100, 100),
            })
        
        return self.health <= 0
    
    def off_screen(self):
        """Check if boss has left the screen"""
        return self.y > 900 or self.y < -200
    
    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, 
                          self.size, self.size)
    
    def draw(self, surface):
        """Draw boss with visual effects"""
        try:
            # Draw glow halo
            for offset in range(15, 0, -3):
                alpha = int(255 * (15 - offset) / 15 * 0.3)
                glow_color = tuple(min(255, int(c * 0.8)) for c in self.color)
                pygame.draw.circle(surface, glow_color, 
                                 (int(self.x), int(self.y)), 
                                 self.size // 2 + offset, 1)
            
            # Draw main boss body with rotation effect
            self._draw_boss_sprite(surface)
            
            # Draw attack particles
            for particle in self.attack_particles:
                pygame.draw.circle(surface, particle['color'],
                                 (int(particle['x']), int(particle['y'])),
                                 particle['size'])
            
            # Draw health bar above boss
            bar_width = 120
            bar_height = 15
            bar_x = self.x - bar_width // 2
            bar_y = self.y - self.size // 2 - 30
            
            # Background
            pygame.draw.rect(surface, (50, 50, 50), 
                           (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4))
            
            # Health fill
            fill_width = int(bar_width * self.health_bar_display)
            health_color = (
                255 - int(255 * self.health_bar_display),
                int(100 * self.health_bar_display),
                50
            )
            pygame.draw.rect(surface, health_color, 
                           (bar_x, bar_y, fill_width, bar_height))
            
            # Border
            pygame.draw.rect(surface, self.color, 
                           (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4), 2)
            
        except Exception as e:
            print(f"Boss draw error: {e}")
    
    def _draw_boss_sprite(self, surface):
        """Draw the boss sprite based on type"""
        try:
            if self.boss_type == 'destroyer':
                self._draw_destroyer(surface)
            elif self.boss_type == 'interceptor':
                self._draw_interceptor(surface)
            elif self.boss_type == 'commander':
                self._draw_commander(surface)
            elif self.boss_type == 'apex':
                self._draw_apex(surface)
            elif self.boss_type == 'mothership':
                self._draw_mothership(surface)
            else:
                self._draw_destroyer(surface)
        except Exception as e:
            print(f"Boss sprite draw error: {e}")
    
    def _draw_destroyer(self, surface):
        """Draw destroyer boss - heavy and blocky"""
        x, y = int(self.x), int(self.y)
        size = self.size
        
        # Main hull
        pygame.draw.polygon(surface, self.color, [
            (x, y - size // 2),
            (x + size // 2, y),
            (x, y + size // 2),
            (x - size // 2, y),
        ])
        
        # Core glow
        pygame.draw.circle(surface, (255, 100, 0), (x, y), size // 4)
        
        # Weapon ports
        pygame.draw.circle(surface, (255, 200, 0), (x - 15, y - 10), 4)
        pygame.draw.circle(surface, (255, 200, 0), (x + 15, y - 10), 4)
    
    def _draw_interceptor(self, surface):
        """Draw interceptor boss - sleek and fast"""
        x, y = int(self.x), int(self.y)
        size = self.size
        
        # Sleek profile
        pygame.draw.polygon(surface, self.color, [
            (x + size // 2, y),
            (x, y + size // 3),
            (x - size // 2, y),
            (x, y - size // 3),
        ])
        
        # Speed lines
        for i in range(1, 4):
            pygame.draw.line(surface, self.color, 
                           (x - size // 2 - i * 3, y - i * 2),
                           (x - size // 2 - i * 3, y + i * 2), 1)
    
    def _draw_commander(self, surface):
        """Draw commander boss - imposing"""
        x, y = int(self.x), int(self.y)
        size = self.size
        
        # Large central hull
        pygame.draw.polygon(surface, self.color, [
            (x, y - size // 2),
            (x + size // 2, y + size // 4),
            (x, y + size // 2),
            (x - size // 2, y + size // 4),
        ])
        
        # Command bridge
        pygame.draw.polygon(surface, (255, 150, 0), [
            (x - 5, y - 15),
            (x + 5, y - 15),
            (x + 7, y - 5),
            (x - 7, y - 5),
        ])
        
        # Weapon arrays
        for offset in [-15, 15]:
            pygame.draw.circle(surface, (255, 100, 0), (x + offset, y), 5)
    
    def _draw_apex(self, surface):
        """Draw apex hunter boss - sleek and deadly"""
        x, y = int(self.x), int(self.y)
        size = self.size
        
        # Diamond shape - deadly
        pygame.draw.polygon(surface, self.color, [
            (x, y - size // 2),
            (x + size // 2, y),
            (x, y + size // 2),
            (x - size // 2, y),
        ])
        
        # Glowing core
        glowing_color = (int(self.color[0] * 0.7 + 200 * 0.3),
                        int(self.color[1] * 0.7 + 0 * 0.3),
                        int(self.color[2] * 0.7 + 255 * 0.3))
        pygame.draw.circle(surface, glowing_color, (x, y), size // 3)
        
        # Hunter markings
        pygame.draw.circle(surface, (255, 50, 100), (x - 10, y - 10), 3)
        pygame.draw.circle(surface, (255, 50, 100), (x + 10, y - 10), 3)
    
    def _draw_mothership(self, surface):
        """Draw mothership boss - MASSIVE"""
        x, y = int(self.x), int(self.y)
        size = self.size
        
        # Massive hull
        pygame.draw.rect(surface, self.color, 
                       (x - size, y - size // 2, size * 2, size), 0)
        
        # Core reactors
        pygame.draw.circle(surface, (255, 100, 100), (x - size // 2, y), size // 3)
        pygame.draw.circle(surface, (100, 200, 255), (x + size // 2, y), size // 3)
        
        # Weapon turrets
        for turret_y in [y - size // 4, y, y + size // 4]:
            pygame.draw.circle(surface, (255, 150, 0), (x - size, turret_y), 4)
            pygame.draw.circle(surface, (255, 150, 0), (x + size, turret_y), 4)
        
        # Command bridge
        pygame.draw.polygon(surface, (200, 200, 0), [
            (x - 20, y - 20),
            (x + 20, y - 20),
            (x + 15, y - 5),
            (x - 15, y - 5),
        ])
    
    def get_display_name(self):
        """Get the boss display name"""
        return self.boss_data['name']
    
    def get_difficulty_rating(self):
        """Get difficulty rating (stars)"""
        return int(self.boss_data['difficulty'])


# Create boss based on wave progression
def create_boss_for_wave(wave, base_difficulty=1.0):
    """Factory function to create appropriate boss for wave"""
    from story import get_boss_type_for_wave
    
    boss_type = get_boss_type_for_wave(wave)
    
    # Determine position
    x = random.randint(200, 800)
    y = -100
    
    return EnhancedBoss(x, y, wave, boss_type, base_difficulty)

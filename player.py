import pygame
from settings import PLAYER_SIZE, PLAYER_SPEED, PLAYER_COOLDOWN, BLUE, WIDTH, HEIGHT
from space_graphics import RocketGraphics

class Player:
    def __init__(self, avatar_type='falcon'):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.size = PLAYER_SIZE
        self.speed = PLAYER_SPEED
        self.cooldown = 0
        self.fire_rate_boost = 0
        self.avatar_type = avatar_type
        self.glow_effect = 0
        self.animation_frame = 0
        self.bob_offset = 0
        self.multi_shot_text_shown = False  # Flag to prevent spam
        self.is_mini = False  # Phoenix revive mode - smaller scout version
        
        # Avatar names map
        self.avatar_names = {
            'falcon': 'Falcon Rocket',
            'nova': 'Nova Laser Ship',
            'shadow': 'Shadow Fighter',
            'titan': 'Titan Cruiser',
            'phoenix': 'Phoenix Explorer'
        }
        
        # Avatar-specific stats
        self.avatar_stats = {
            'falcon': {'speed_mult': 0.85, 'health_bonus': 2, 'damage_mult': 1.0, 'shield_regen': 0.15},
            'nova': {'speed_mult': 0.7, 'health_bonus': 0, 'damage_mult': 1.5, 'multi_shot': True},
            'shadow': {'speed_mult': 1.3, 'health_bonus': -1, 'damage_mult': 0.8, 'dash': True},
            'titan': {'speed_mult': 0.6, 'health_bonus': 3, 'damage_mult': 1.2, 'tank_mode': True},
            'phoenix': {'speed_mult': 1.0, 'health_bonus': 0, 'damage_mult': 1.0, 'revive': True}
        }
        
        self.stats = self.avatar_stats.get(avatar_type, self.avatar_stats['falcon'])
        self.speed = PLAYER_SPEED * self.stats['speed_mult']
        self.phoenix_revived = False

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.size:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < HEIGHT - self.size:
            self.y += self.speed

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1
        if self.fire_rate_boost > 0:
            self.fire_rate_boost -= 1
        self.glow_effect = (self.glow_effect + 1) % 60
        self.animation_frame = (self.animation_frame + 1) % 60
        self.bob_offset = 3 * abs((self.animation_frame - 30) / 30)

    def can_shoot(self):
        return self.cooldown <= 0

    def shoot(self):
        if self.can_shoot():
            boost_multiplier = 0.5 if self.fire_rate_boost > 0 else 1.0
            self.cooldown = int(PLAYER_COOLDOWN * boost_multiplier)

    def draw(self, screen):
        """Draw rocket with glow and boost effects"""
        try:
            import math
            
            # Animated glow effect
            glow_radius = int(15 + 8 * (abs(30 - self.glow_effect) / 30))
            glow_colors = {
                'falcon': (100, 200, 255),
                'nova': (200, 100, 255),
                'shadow': (255, 100, 200),
                'titan': (100, 255, 200),
                'phoenix': (255, 150, 50)
            }
            glow_color = glow_colors.get(self.avatar_type, (100, 150, 255))
            pygame.draw.circle(screen, glow_color, (int(self.x + self.size // 2), int(self.y + self.size // 2)), glow_radius, 2)
            
            # Draw rocket based on type (with bob animation)
            draw_y = self.y + self.bob_offset
            draw_size = int(self.size * 0.6) if self.is_mini else self.size
            
            if self.is_mini:
                # Mini phoenix scout version
                RocketGraphics.draw_mini_phoenix(screen, self.x + self.size // 4, draw_y, draw_size, glow_color)
            elif self.avatar_type == 'falcon':
                RocketGraphics.draw_falcon_rocket(screen, self.x, draw_y, self.size, glow_color)
            elif self.avatar_type == 'nova':
                RocketGraphics.draw_nova_laser(screen, self.x, draw_y, self.size, glow_color)
            elif self.avatar_type == 'shadow':
                RocketGraphics.draw_shadow_fighter(screen, self.x, draw_y, self.size, glow_color)
            elif self.avatar_type == 'titan':
                RocketGraphics.draw_titan_cruiser(screen, self.x, draw_y, self.size, glow_color)
            elif self.avatar_type == 'phoenix':
                RocketGraphics.draw_phoenix_explorer(screen, self.x, draw_y, self.size, glow_color)
            else:
                RocketGraphics.draw_falcon_rocket(screen, self.x, draw_y, self.size, glow_color)
            
            # Draw fire rate boost effect
            if self.fire_rate_boost > 0:
                # Boost aura
                pulse = math.sin(self.animation_frame * 0.2) * 0.3 + 0.7
                pygame.draw.circle(screen, (255, 255, 0), (int(self.x + self.size // 2), int(draw_y + self.size // 2)), 
                                  int(self.size // 1.5 * pulse), 2)
                # Boost ring
                pygame.draw.circle(screen, (255, 200, 0), (int(self.x + self.size // 2), int(draw_y + self.size // 2)), 
                                  int(self.size // 1.2), 1)
            
            # Draw mini indicator text (without emoji to avoid rendering issues)
            if self.is_mini:
                font_tiny = pygame.font.SysFont(None, 16)
                mini_text = font_tiny.render("SCOUT", True, (255, 150, 50))
                screen.blit(mini_text, (int(self.x + self.size // 2 - 20), int(draw_y + self.size + 5)))
        except Exception as e:
            # Silent fail on render - don't crash
            pass

    
    def get_rect(self):
        """Return collision rectangle"""
        if self.is_mini:
            # Mini scout is 60% size, positioned accordingly
            mini_size = int(self.size * 0.6)
            return pygame.Rect(self.x + self.size // 4, self.y, mini_size, mini_size)
        return pygame.Rect(self.x, self.y, self.size, self.size)

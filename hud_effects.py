"""
Enhanced HUD (Heads-Up Display) with advanced visual animations
"""
import pygame
import math


class AnimatedHUD:
    """Advanced HUD system with animations and visual effects"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.score_pulse = 0
        self.health_pulse = 0
        self.combo_pulse = 0
        self.wave_flash = 0
        
    def update(self):
        """Update HUD animation values"""
        self.score_pulse = (self.score_pulse + 0.03) % (2 * math.pi)
        self.health_pulse = (self.health_pulse + 0.05) % (2 * math.pi)
        self.combo_pulse = (self.combo_pulse + 0.04) % (2 * math.pi)
        if self.wave_flash > 0:
            self.wave_flash -= 1
    
    def draw_score_display(self, screen, score, font):
        """Draw animated score display"""
        pulse_intensity = 3 + int(2 * math.sin(self.score_pulse))
        
        # Pulsing box background
        box_rect = pygame.Rect(5, 5, 200, 115)
        
        # Glow effect
        for i in range(pulse_intensity, 0, -1):
            glow_color = tuple(min(int(c * (pulse_intensity - i) / pulse_intensity * 0.3), 255) for c in (0, 150, 255))
            pygame.draw.rect(screen, glow_color, box_rect.inflate(i * 2, i * 2), 1)
        
        # Box with gradient effect
        pygame.draw.rect(screen, (20, 40, 60), box_rect, 0)
        pygame.draw.rect(screen, (0, 150, 255), box_rect, 2)
        
        # Score text with glow
        score_text = font.render(f"Score: {score}", True, (0, 255, 100))
        text_glow = font.render(f"Score: {score}", True, tuple(min(int(c * 0.5), 255) for c in (0, 255, 100)))
        screen.blit(text_glow, (22, 22))
        screen.blit(score_text, (20, 20))
    
    def draw_health_display(self, screen, health, max_health, font, bar_color=(0, 255, 0)):
        """Draw animated health bar"""
        bar_width = 300
        bar_height = 30
        bar_x = self.width // 2 - bar_width // 2
        bar_y = self.height - 50
        
        # Pulsing glow based on health status
        if health < max_health // 3:
            pulse = 2 + int(3 * math.sin(self.health_pulse * 2))  # Fast pulse when critical
            glow_color = (255, 0, 0)
        elif health < max_health // 2:
            pulse = 1 + int(2 * math.sin(self.health_pulse))
            glow_color = (255, 165, 0)
        else:
            pulse = 1 + int(1.5 * math.sin(self.health_pulse * 0.5))
            glow_color = (0, 255, 0)
        
        # Outer glow rings
        for i in range(pulse, 0, -1):
            glow_alpha = int(100 * (pulse - i) / pulse)
            glow_color_fade = tuple(min(int(c * (pulse - i) / pulse * 0.5), 255) for c in glow_color)
            pygame.draw.rect(screen, glow_color_fade, (bar_x - i * 2, bar_y - i * 2, bar_width + i * 4, bar_height + i * 4), 1)
        
        # Bar background
        pygame.draw.rect(screen, (60, 60, 60), (bar_x - 5, bar_y - 5, bar_width + 10, bar_height + 10))
        pygame.draw.rect(screen, (30, 30, 30), (bar_x, bar_y, bar_width, bar_height))
        
        # Health fill with gradient effect
        health_ratio = health / max(1, max_health)
        fill_width = int(bar_width * health_ratio)
        
        # Gradient bar (brighter at full, dimmer at empty)
        for x in range(fill_width):
            progress = x / max(1, fill_width)
            bar_color_at_x = tuple(int(c * progress + glow_color[i] * (1 - progress)) for i, c in enumerate(bar_color))
            pygame.draw.line(screen, bar_color_at_x, (bar_x + x, bar_y), (bar_x + x, bar_y + bar_height))
        
        # Bar outline
        pygame.draw.rect(screen, glow_color, (bar_x, bar_y, bar_width, bar_height), 3)
        pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height), 1)
        
        # Health text
        health_text = font.render(f"HEALTH: {health}/{max_health}", True, glow_color)
        screen.blit(health_text, (bar_x + 60, bar_y + 5))
    
    def draw_wave_display(self, screen, wave, font):
        """Draw animated wave indicator"""
        box_x = self.width - 290
        box_y = 5
        box_width = 285
        box_height = 75
        
        # Wave flash animation
        if wave % 10 == 0 or wave % 10 == 1:  # Flash every 10 waves
            self.wave_flash = 30
        
        flash_intensity = self.wave_flash / 30 if self.wave_flash > 0 else 0
        
        # Pulsing glow
        glow_size = int(3 * flash_intensity)
        for i in range(glow_size, 0, -1):
            glow_color = (0 + int(100 * flash_intensity), 150 - int(50 * flash_intensity), 255 - int(100 * flash_intensity))
            pygame.draw.rect(screen, glow_color, (box_x - i, box_y - i, box_width + i * 2, box_height + i * 2), 1)
        
        # Box
        box_bg = (20, 40, 60)
        box_border = (0 + int(150 * flash_intensity), 150 - int(50 * flash_intensity), 255 - int(100 * flash_intensity))
        pygame.draw.rect(screen, box_bg, (box_x, box_y, box_width, box_height), 0)
        pygame.draw.rect(screen, box_border, (box_x, box_y, box_width, box_height), 2)
        
        # Wave text with size variation
        font_size_bonus = int(3 * flash_intensity)
        wave_color = (0 + int(200 * flash_intensity), 200 - int(100 * flash_intensity), 255)
        wave_text = font.render(f"Wave: {wave}", True, wave_color)
        screen.blit(wave_text, (box_x + 20, box_y + 20))
    
    def draw_indicator_bars(self, screen, weapon_level, shield_charge, max_shield, font):
        """Draw upgrade indicator bars"""
        bar_y = 100
        bar_height = 20
        bar_x = 20
        
        # Weapon level bar
        pygame.draw.rect(screen, (50, 50, 0), (bar_x, bar_y, 100, bar_height))
        pygame.draw.rect(screen, (255, 200, 0), (bar_x, bar_y, int(100 * (weapon_level / 5)), bar_height))
        pygame.draw.rect(screen, (200, 150, 0), (bar_x, bar_y, 100, bar_height), 2)
        
        weapon_text = font.render(f"WPN: {weapon_level}", True, (255, 200, 0))
        screen.blit(weapon_text, (bar_x + 110, bar_y))
        
        # Shield bar
        bar_y += 30
        pygame.draw.rect(screen, (0, 50, 100), (bar_x, bar_y, 100, bar_height))
        shield_fill = int(100 * (shield_charge / max_shield)) if max_shield > 0 else 0
        pygame.draw.rect(screen, (0, 150, 255), (bar_x, bar_y, shield_fill, bar_height))
        pygame.draw.rect(screen, (0, 100, 200), (bar_x, bar_y, 100, bar_height), 2)
        
        shield_text = font.render(f"SHD: {shield_charge}/{max_shield}", True, (0, 150, 255))
        screen.blit(shield_text, (bar_x + 110, bar_y))


class ComboDamageVisualizer:
    """Shows combo damage bonus with visual indicators"""
    
    def __init__(self):
        self.last_combo = 0
        self.combo_popup_timer = 0
        self.popup_x = 0
        self.popup_y = 0
    
    def update(self, combo):
        """Track combo changes"""
        if combo > self.last_combo and combo % 3 == 0:
            self.combo_popup_timer = 30
        self.last_combo = combo
        
        if self.combo_popup_timer > 0:
            self.combo_popup_timer -= 1
    
    def draw_combo_popup(self, screen, combo, x, y, font):
        """Draw pop-up combo bonus indicator"""
        if self.combo_popup_timer > 0:
            progress = 1 - (self.combo_popup_timer / 30)
            alpha = int(255 * (1 - progress))
            combo_bonus = (combo // 3) * 0.2
            
            popup_y = y - int(progress * 50)  # Float upward
            
            bonus_text = font.render(f"+{combo_bonus:.1f}x BONUS!", True, (255, 215, 0))
            screen.blit(bonus_text, (x - 50, int(popup_y)))


class WaveIndicator:
    """Shows wave progression with visual intensity"""
    
    def __init__(self):
        self.last_wave = 0
        self.wave_transition_timer = 0
    
    def update(self, wave):
        """Trigger animation on wave change"""
        if wave > self.last_wave:
            self.wave_transition_timer = 60
            self.last_wave = wave
        
        if self.wave_transition_timer > 0:
            self.wave_transition_timer -= 1
    
    def draw_wave_transition(self, screen, wave, width, height, font_menu):
        """Draw wave transition animation"""
        if self.wave_transition_timer > 0:
            progress = 1 - (self.wave_transition_timer / 60)
            
            # Fade in wave number
            alpha = int(255 * progress)
            
            wave_text = font_menu.render(f"WAVE {wave}", True, (0, 255, 150))
            wave_text.set_alpha(alpha)
            
            text_rect = wave_text.get_rect(center=(width // 2, height // 2))
            screen.blit(wave_text, text_rect)
            
            # Expanding circle effect
            circle_radius = int(100 + progress * 100)
            circle_color = (0, 255, 150)
            circle_color_fade = tuple(int(c * (1 - progress) * 0.3) for c in circle_color)
            pygame.draw.circle(screen, circle_color_fade, (width // 2, height // 2), circle_radius, 2)

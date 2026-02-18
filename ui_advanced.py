"""
🎮 ADVANCED UI SYSTEM - Professional Game Interface
Complete redesign with story integration, better layouts, and information display
"""

import pygame
import math
from story import CAMPAIGN_PHASES, AVATAR_ABILITIES

class AdvancedUIRenderer:
    """High-quality UI rendering system"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.story_text_display_queue = []
        self.milestone_display = None
        self.milestone_timer = 0
        self.phase_indicator_show = True
        self.phase_indicator_timer = 0
    
    def render_hud(self, screen, player, wave, score, combo, health, max_health, 
                   avatar_type, difficulty, special_states=None):
        """Render main HUD with all information"""
        
        # Top-left: Player status panel
        self._render_player_status(screen, player, avatar_type, health, max_health)
        
        # Top-right: Score and progression info
        self._render_score_panel(screen, score, wave, combo)
        
        # Bottom-center: Health bar with enhanced style
        self._render_health_bar(screen, health, max_health)
        
        # Center-right: Current phase and objectives
        self._render_phase_info(screen, wave)
        
        # Top: Story text if available
        self._render_story_text(screen)
        
        # Center: Milestone notifications
        if self.milestone_display:
            self._render_milestone(screen)
    
    def _render_player_status(self, screen, player, avatar_type, health, max_health):
        """Render player status in top-left"""
        try:
            avatar_data = AVATAR_ABILITIES.get(avatar_type, AVATAR_ABILITIES['falcon'])
            
            # Panel background
            panel_width = 280
            panel_height = 120
            pygame.draw.rect(screen, (10, 20, 40), (5, 5, panel_width, panel_height))
            pygame.draw.rect(screen, avatar_data['color'], (5, 5, panel_width, panel_height), 2)
            
            # Avatar title
            font_title = pygame.font.SysFont(None, 24, bold=True)
            font_text = pygame.font.SysFont(None, 18)
            
            title = font_title.render(avatar_data['name'].upper(), True, avatar_data['color'])
            subtitle = font_text.render(f"{avatar_data['title']}", True, (150, 200, 255))
            ability = font_text.render(f"🔸 {avatar_data['ability']}", True, (200, 255, 200))
            
            screen.blit(title, (20, 15))
            screen.blit(subtitle, (20, 40))
            screen.blit(ability, (20, 60))
            
            # Perk display
            perk = font_text.render(f"✓ {avatar_data['special_perk']}", True, (255, 200, 100))
            screen.blit(perk, (20, 85))
            
        except Exception as e:
            print(f"Player status render error: {e}")
    
    def _render_score_panel(self, screen, score, wave, combo):
        """Render score and wave info in top-right"""
        try:
            font_large = pygame.font.SysFont(None, 32, bold=True)
            font_small = pygame.font.SysFont(None, 20)
            
            panel_width = 280
            panel_height = 120
            panel_x = self.width - panel_width - 5
            
            # Panel background
            pygame.draw.rect(screen, (10, 20, 40), (panel_x, 5, panel_width, panel_height))
            pygame.draw.rect(screen, (0, 255, 100), (panel_x, 5, panel_width, panel_height), 2)
            
            # Wave indicator with progression
            wave_text = font_large.render(f"WAVE {wave}", True, (0, 255, 100))
            screen.blit(wave_text, (panel_x + 15, 15))
            
            # Score
            score_text = font_large.render(f"${score:,}", True, (255, 215, 0))
            screen.blit(score_text, (panel_x + 15, 50))
            
            # Combo counter
            combo_color = (255, 100, 100) if combo == 0 else (255, 165, 0) if combo < 10 else (100, 255, 100)
            combo_display = f"×{combo} COMBO" if combo > 0 else "READY"
            combo_text = font_small.render(combo_display, True, combo_color)
            screen.blit(combo_text, (panel_x + 15, 88))
            
        except Exception as e:
            print(f"Score panel render error: {e}")
    
    def _render_health_bar(self, screen, health, max_health):
        """Render main health bar at bottom"""
        try:
            bar_width = 400
            bar_height = 40
            bar_x = self.width // 2 - bar_width // 2
            bar_y = self.height - 80
            
            # Health color gradient
            health_ratio = max(0, health / max(1, max_health))
            if health_ratio > 0.5:
                bar_color = (0, 255, int(255 * (1 - health_ratio * 2)))  # Green to yellow
            else:
                bar_color = (255, int(255 * (health_ratio * 2)), 0)  # Yellow to red
            
            # Background
            pygame.draw.rect(screen, (30, 30, 30), (bar_x - 5, bar_y - 5, bar_width + 10, bar_height + 10))
            pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
            
            # Health fill with gradient
            fill_width = int(bar_width * health_ratio)
            pygame.draw.rect(screen, bar_color, (bar_x, bar_y, fill_width, bar_height))
            
            # Damage flash effect
            if health <= max_health * 0.25:
                danger_flash = int(255 * (0.5 + 0.5 * math.sin(pygame.time.get_ticks() / 100)))
                pygame.draw.rect(screen, (255, 0, 0, danger_flash), 
                               (bar_x, bar_y, bar_width, bar_height), 3)
            else:
                pygame.draw.rect(screen, bar_color, (bar_x, bar_y, bar_width, bar_height), 3)
            
            # Health text
            font_large = pygame.font.SysFont(None, 28, bold=True)
            health_display = f"HEALTH: {health}/{max_health}"
            health_text = font_large.render(health_display, True, (255, 255, 255))
            screen.blit(health_text, (bar_x + 20, bar_y + 8))
            
            # Shield indicator if applicable
            font_small = pygame.font.SysFont(None, 18)
            shield_text = font_small.render("🛡️ SHIELD ACTIVE", True, (100, 200, 255))
            screen.blit(shield_text, (bar_x + 220, bar_y + 12))
            
        except Exception as e:
            print(f"Health bar render error: {e}")
    
    def _render_phase_info(self, screen, wave):
        """Render current phase and objectives"""
        try:
            from story import get_current_phase
            
            phase_id, phase_data = get_current_phase(wave)
            
            # Panel on right side
            panel_width = 300
            panel_height = 200
            panel_x = self.width - panel_width - 5
            panel_y = self.height - panel_height - 90
            
            pygame.draw.rect(screen, (20, 30, 50), (panel_x, panel_y, panel_width, panel_height))
            pygame.draw.rect(screen, (100, 150, 255), (panel_x, panel_y, panel_width, panel_height), 2)
            
            # Phase title
            font_title = pygame.font.SysFont(None, 20, bold=True)
            font_text = pygame.font.SysFont(None, 14)
            
            phase_text = font_title.render(f"📍 {phase_data['name']}", True, (100, 150, 255))
            screen.blit(phase_text, (panel_x + 10, panel_y + 8))
            
            # Objectives
            objectives = phase_data.get('objectives', [])
            y_offset = 35
            for i, obj in enumerate(objectives[:2]):  # Show first 2 objectives
                obj_text = font_text.render(f"• {obj[:25]}", True, (200, 200, 200))
                screen.blit(obj_text, (panel_x + 15, panel_y + y_offset))
                y_offset += 20
            
            # Progress bar
            progress_y = panel_y + panel_height - 30
            progress_width = panel_width - 20
            wave_min, wave_max = phase_data['waves']
            progress = ((wave - wave_min) / (wave_max - wave_min + 1))
            
            pygame.draw.rect(screen, (30, 30, 30), (panel_x + 10, progress_y, progress_width, 15))
            pygame.draw.rect(screen, (0, 255, 100), (panel_x + 10, progress_y, int(progress_width * progress), 15))
            pygame.draw.rect(screen, (100, 150, 255), (panel_x + 10, progress_y, progress_width, 15), 1)
            
            # Progress text
            progress_text = font_text.render(f"Phase {wave}/{wave_max}", True, (200, 200, 200))
            screen.blit(progress_text, (panel_x + 15, progress_y - 20))
            
        except Exception as e:
            print(f"Phase info render error: {e}")
    
    def _render_story_text(self, screen):
        """Render story text notifications at top"""
        try:
            if self.story_text_display_queue:
                story_item = self.story_text_display_queue[0]
                story_item['lifetime'] -= 1
                
                if story_item['lifetime'] <= 0:
                    self.story_text_display_queue.pop(0)
                    return
                
                # Calculate fade
                fade_duration = 15
                if story_item['lifetime'] > story_item['max_lifetime'] - fade_duration:
                    alpha = int(255 * (story_item['lifetime'] / fade_duration))
                elif story_item['lifetime'] < fade_duration:
                    alpha = int(255 * (story_item['lifetime'] / fade_duration))
                else:
                    alpha = 255
                
                # Create text surface with transparency
                text_lines = story_item['text'].split('\n')
                font = pygame.font.SysFont(None, 24)
                
                y_pos = 120
                for line in text_lines:
                    if line:
                        text_surf = font.render(line, True, story_item['color'])
                        screen.blit(text_surf, (self.width // 2 - text_surf.get_width() // 2, y_pos))
                        y_pos += 30
        
        except Exception as e:
            print(f"Story text render error: {e}")
    
    def _render_milestone(self, screen):
        """Render milestone achievement"""
        try:
            if self.milestone_display and self.milestone_timer > 0:
                self.milestone_timer -= 1
                
                milestone_text = self.milestone_display['text']
                milestone_reward = self.milestone_display['reward']
                
                # Large centered notification
                font_large = pygame.font.SysFont(None, 60, bold=True)
                font_small = pygame.font.SysFont(None, 28)
                
                # Rainbow color animation
                hue = (self.milestone_timer / 120) * 360
                color = self._hsv_to_rgb(hue, 1.0, 1.0)
                
                # Draw milestone box
                box_width = 500
                box_height = 150
                box_x = self.width // 2 - box_width // 2
                box_y = self.height // 2 - box_height // 2
                
                pygame.draw.rect(screen, (20, 20, 40), (box_x, box_y, box_width, box_height))
                pygame.draw.rect(screen, color, (box_x, box_y, box_width, box_height), 4)
                
                # Text
                text = font_large.render(milestone_text, True, color)
                reward_text = font_small.render(f"+{milestone_reward} BONUS POINTS!", True, (255, 215, 0))
                
                screen.blit(text, (box_x + 20, box_y + 35))
                screen.blit(reward_text, (box_x + 20, box_y + 95))
        
        except Exception as e:
            print(f"Milestone render error: {e}")
    
    def add_story_text(self, text, color=(255, 200, 100), duration=120):
        """Add story text to display queue"""
        self.story_text_display_queue.append({
            'text': text,
            'color': color,
            'lifetime': duration,
            'max_lifetime': duration,
        })
    
    def show_milestone(self, text, reward):
        """Show milestone notification"""
        self.milestone_display = {'text': text, 'reward': reward}
        self.milestone_timer = 120
    
    @staticmethod
    def _hsv_to_rgb(h, s, v):
        """Convert HSV to RGB"""
        import colorsys
        return tuple(int(c * 255) for c in colorsys.hsv_to_rgb(h / 360, s, v))


class MenuRenderer:
    """Redesigned menu UI system"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.selected_index = 0
        self.animation_timer = 0
    
    def render_main_menu(self, screen, high_score, best_combo, best_wave):
        """Render main menu with story title"""
        self.animation_timer += 1
        
        # Starfield background
        font_title = pygame.font.SysFont(None, 80, bold=True)
        font_subtitle = pygame.font.SysFont(None, 40)
        font_text = pygame.font.SysFont(None, 24)
        
        # Main title with glow
        title = "⚔️ SURVIVAL GAME"
        subtitle = "Adventure Edition"
        
        color = (0, 200 + int(55 * math.sin(self.animation_timer / 30)), 255)
        
        title_text = font_title.render(title, True, color)
        subtitle_text = font_subtitle.render(subtitle, True, (100, 200, 255))
        
        screen.blit(title_text, (self.width // 2 - title_text.get_width() // 2, 40))
        screen.blit(subtitle_text, (self.width // 2 - subtitle_text.get_width() // 2, 130))
        
        # Stats panel
        stats_y = 220
        stat_items = [
            (f"⭐ HIGH SCORE", f"{high_score:,}", (255, 215, 0)),
            (f"🔥 BEST COMBO", f"{best_combo}", (255, 100, 100)),
            (f"🌊 BEST WAVE", f"{best_wave}", (100, 150, 255)),
        ]
        
        for label, value, stat_color in stat_items:
            label_text = font_text.render(label, True, stat_color)
            value_text = font_subtitle.render(value, True, (255, 255, 255))
            
            screen.blit(label_text, (200, stats_y))
            screen.blit(value_text, (700, stats_y))
            stats_y += 60
        
        # Menu options
        option_y = 520
        options = [
            "▶ PRESS SPACE - START ADVENTURE",
            "[ S ] SETTINGS  |  [ Q ] QUIT",
        ]
        
        for option in options:
            opt_text = font_text.render(option, True, (150, 200, 255))
            screen.blit(opt_text, (self.width // 2 - opt_text.get_width() // 2, option_y))
            option_y += 50

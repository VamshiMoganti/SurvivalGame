import pygame
import math
import random

class Weapon:
    """Weapon upgrade system"""
    def __init__(self):
        self.fire_rate = 15  # Lower = faster
        self.damage = 1
        self.spread = 0  # Number of extra bullets
        self.color = (100, 200, 255)
        self.width = 5
        self.height = 10

    def upgrade_fire_rate(self):
        self.fire_rate = max(5, int(self.fire_rate * 0.85))
        return True

    def upgrade_damage(self):
        self.damage += 1
        return True

    def upgrade_spread(self):
        if self.spread < 2:
            self.spread += 1
            return True
        return False

    def get_level(self):
        return {
            'fire_rate': int((15 - self.fire_rate) / 2),
            'damage': self.damage,
            'spread': self.spread
        }


class Shield:
    """Shield system - absorbs damage"""
    def __init__(self, max_charge=2):  # Default 2 charge - more balanced
        self.max_charge = max_charge
        self.current_charge = max_charge
        self.regen_rate = 0.05  # Reduced from 0.1
        self.active = True
        self.regen_cooldown = 0  # Don't regen immediately after damage

    def take_damage(self, amount=1):
        """Absorb damage, return remaining damage"""
        if self.current_charge >= amount:
            self.current_charge -= amount
            self.regen_cooldown = 120  # Wait 2 seconds before regenerating
            return 0
        else:
            remaining = amount - self.current_charge
            self.current_charge = 0
            self.regen_cooldown = 120  # Wait 2 seconds before regenerating
            return remaining

    def update(self):
        """Regenerate shield after cooldown"""
        if self.regen_cooldown > 0:
            self.regen_cooldown -= 1
        elif self.current_charge < self.max_charge:
            self.current_charge = min(self.max_charge, self.current_charge + self.regen_rate)
        
        # Auto-break shield if completely depleted for too long (stale state prevention)
        if self.current_charge <= 0 and random.random() < 0.01:
            self.regen_cooldown = max(0, self.regen_cooldown - 10)

    def is_active(self):
        return self.current_charge > 0

    def draw(self, screen, x, y, size):
        if self.active and self.current_charge > 0:
            radius = int(size // 1.5)
            color = (0, 255, 200)
            pygame.draw.circle(screen, color, (int(x + size // 2), int(y + size // 2)), radius, 3)


class Achievement:
    """Achievement system"""
    ACHIEVEMENTS = {
        'first_blood': {'name': 'First Blood', 'desc': 'Defeat your first enemy', 'icon': '🗡️'},
        'combo_10': {'name': 'Combo Master', 'desc': 'Reach 10 combo', 'icon': '⚡'},
        'score_100': {'name': 'Century', 'desc': 'Reach 100 score', 'icon': '💯'},
        'boss_slayer': {'name': 'Boss Slayer', 'desc': 'Defeat a boss', 'icon': '👑'},
        'wave_10': {'name': 'Wave Rider', 'desc': 'Reach wave 10', 'icon': '🌊'},
        'speed_demon': {'name': 'Speed Demon', 'desc': 'Reach 25 combo without missing', 'icon': '🔥'},
    }

    def __init__(self):
        self.unlocked = set()

    def unlock(self, achievement_id):
        if achievement_id not in self.unlocked and achievement_id in self.ACHIEVEMENTS:
            self.unlocked.add(achievement_id)
            return self.ACHIEVEMENTS[achievement_id]
        return None

    def check_achievements(self, score, combo, wave, boss_killed, max_combo):
        """Check and unlock achievements"""
        unlocked_list = []
        
        if score > 0 and 'first_blood' not in self.unlocked:
            unlocked_list.append(self.unlock('first_blood'))
        
        if combo >= 10 and 'combo_10' not in self.unlocked:
            unlocked_list.append(self.unlock('combo_10'))
        
        if score >= 100 and 'score_100' not in self.unlocked:
            unlocked_list.append(self.unlock('score_100'))
        
        if boss_killed and 'boss_slayer' not in self.unlocked:
            unlocked_list.append(self.unlock('boss_slayer'))
        
        if wave >= 10 and 'wave_10' not in self.unlocked:
            unlocked_list.append(self.unlock('wave_10'))
        
        if max_combo >= 25 and 'speed_demon' not in self.unlocked:
            unlocked_list.append(self.unlock('speed_demon'))
        
        return [a for a in unlocked_list if a is not None]

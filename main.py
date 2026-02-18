import pygame
import sys
import random
import math
from settings import *
from player import Player
from enemy import Enemy, create_random_enemy
from bullet import Bullet
from powerup import PowerUp
from particle import Explosion, FloatingText, CritHitEffect, WaveEffect, LootEffect
from sprites import PlayerAvatar
from space_graphics import RocketGraphics
from scores import load_high_scores, save_high_scores
from boss import Boss
from upgrades import Weapon, Shield, Achievement
from visual_effects import (Nebula, EnergyPulse, ScreenFlash, NeonGlow, 
                            ComboMeterVisual, ScreenTransition, ShieldEffect)
from screen_juice import (ScreenJuice, ParticleExplosion, FloatingNumber, GlowingElement,
                          MotionTrail, ComboVisualizer, ShinyNumber, PulsingBar, StarburstEffect)
import traceback

# Crash logging
CRASH_LOG = "crash_log.txt"
def log_crash(error_msg):
    """Log crashes to file for debugging"""
    with open(CRASH_LOG, "a") as f:
        f.write(f"{error_msg}\n")
        f.write(traceback.format_exc())
        f.write("\n---\n")

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SURVIVAL GAME - Ultimate Edition")

clock = pygame.time.Clock()
font_tiny = pygame.font.SysFont(None, 20)
font_small = pygame.font.SysFont(None, 28)
font_large = pygame.font.SysFont(None, 48)
font_menu = pygame.font.SysFont(None, 64)
font_floating = pygame.font.SysFont(None, 36)
font_title = pygame.font.SysFont(None, 72)

# Star field for background
class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.brightness = random.randint(100, 200)
        self.twinkle_speed = random.uniform(0.01, 0.05)
        self.twinkle_value = 0

    def update(self):
        self.twinkle_value += self.twinkle_speed
        self.brightness = int(100 + 100 * math.sin(self.twinkle_value))

    def draw(self, screen):
        pygame.draw.circle(screen, (self.brightness, self.brightness, self.brightness), (self.x, self.y), 1)

stars = [Star() for _ in range(150)]
nebulae = [
    Nebula(random.randint(-100, WIDTH), random.randint(-100, HEIGHT), 400, 300, (100, 50, 200)),
    Nebula(random.randint(-100, WIDTH), random.randint(-100, HEIGHT), 500, 350, (50, 100, 200)),
    Nebula(random.randint(-100, WIDTH), random.randint(-100, HEIGHT), 450, 320, (200, 50, 100)),
]

def draw_starfield(screen, offset_x=0, offset_y=0):
    """Draw starfield with nebula clouds"""
    # Update and draw nebulae
    for nebula in nebulae:
        nebula.update()
        nebula.draw(screen)
    
    # Update and draw stars with twinkling
    for star in stars:
        star.update()
        star.draw(screen)

def draw_gradient_background(screen):
    """Draw gradient background"""
    for y in range(HEIGHT):
        color_ratio = y / HEIGHT
        r = int(20 * (1 - color_ratio) + 50 * color_ratio)
        g = int(20 * (1 - color_ratio) + 30 * color_ratio)
        b = int(40 * (1 - color_ratio) + 100 * color_ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

def draw_border(screen, color=(0, 255, 255), thickness=3, margin=10):
    """Draw fancy border"""
    pygame.draw.rect(screen, color, (margin, margin, WIDTH - 2*margin, HEIGHT - 2*margin), thickness)
    # Corner accents
    corner_size = 20
    corners = [
        (margin, margin), (WIDTH - margin - corner_size, margin),
        (margin, HEIGHT - margin - corner_size), (WIDTH - margin - corner_size, HEIGHT - margin - corner_size)
    ]
    for cx, cy in corners:
        pygame.draw.rect(screen, color, (cx, cy, corner_size, corner_size), thickness)

AVATARS = [
    ('falcon', 'Falcon Rocket', 'Fast and agile with extra shield'),
    ('nova', 'Nova Laser', 'Powerful multi-shot energy blaster'),
    ('shadow', 'Shadow Fighter', 'Rapid ultra-fast interceptor'),
    ('titan', 'Titan Cruiser', 'Heavy tank with armor'),
    ('phoenix', 'Phoenix Explorer', 'Can revive as smaller scout')
]

# Import difficulty settings from settings module
from settings import DIFFICULTIES

def show_main_menu():
    """Show main menu"""
    high_score, best_combo, best_wave = load_high_scores()
    
    while True:
        clock.tick(FPS)
        draw_gradient_background(screen)
        draw_starfield(screen)
        
        # Draw title with glow effect
        title_y = 20
        for offset in range(5, 0, -1):
            shadow_title = font_title.render("SURVIVAL GAME", True, (0, 100 + offset*20, 150 + offset*20))
            screen.blit(shadow_title, (WIDTH // 2 - 290 + offset, title_y + offset))
        
        title = font_title.render("SURVIVAL GAME", True, (0, 255, 255))
        screen.blit(title, (WIDTH // 2 - 285, title_y))
        
        subtitle = font_large.render("🎮 Ultimate Edition", True, (100, 200, 255))
        screen.blit(subtitle, (WIDTH // 2 - 200, 115))
        
        pygame.draw.line(screen, (0, 255, 255), (50, 180), (WIDTH - 50, 180), 3)
        
        # Stats with better formatting
        stat_x = 200
        stat_y = 230
        stats = [
            ("⭐ HIGH SCORE", str(high_score)),
            ("🔥 BEST COMBO", str(best_combo)),
            ("🌊 BEST WAVE", str(best_wave))
        ]
        
        for icon, value in stats:
            label_text = font_large.render(icon + ":", True, (0, 255, 100))
            value_text = font_large.render(value, True, (255, 255, 255))
            screen.blit(label_text, (stat_x, stat_y))
            screen.blit(value_text, (stat_x + 400, stat_y))
            stat_y += 50
        
        pygame.draw.line(screen, (0, 255, 255), (50, 430), (WIDTH - 50, 430), 3)
        
        menu_text = font_large.render("▶ SPACE to Start", True, (0, 255, 150))
        settings_text = font_small.render("[ S ] Settings  |  [ Q ] Quit", True, (150, 200, 255))
        
        screen.blit(menu_text, (WIDTH // 2 - 210, 470))
        screen.blit(settings_text, (WIDTH // 2 - 170, 540))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return 'play'
                if event.key == pygame.K_q:
                    return None

def show_avatar_selection():
    """Show avatar selection menu"""
    selected = 0
    
    while True:
        clock.tick(FPS)
        draw_gradient_background(screen)
        draw_starfield(screen)
        
        title = font_menu.render("⚔️ SELECT YOUR CHARACTER", True, (0, 255, 255))
        screen.blit(title, (WIDTH // 2 - 350, 20))
        
        pygame.draw.line(screen, (0, 255, 255), (50, 95), (WIDTH - 50, 95), 3)
        
        avatar_y = 130
        for i, (avatar_type, avatar_name, avatar_desc) in enumerate(AVATARS):
            is_selected = i == selected
            
            if is_selected:
                pygame.draw.rect(screen, (0, 255, 255), (30, avatar_y - 8, WIDTH - 60, 70), 3)
                bg_rect = pygame.draw.rect(screen, (0, 50, 100), (30, avatar_y - 8, WIDTH - 60, 70))
                color = (0, 255, 255)
            else:
                pygame.draw.rect(screen, (100, 150, 200), (30, avatar_y - 8, WIDTH - 60, 70), 1)
                color = (150, 200, 255)
            
            # Draw avatar
            preview_x = 60
            preview_y = avatar_y
            
            if avatar_type == 'falcon':
                RocketGraphics.draw_falcon_rocket(screen, preview_x, preview_y, 40, color)
            elif avatar_type == 'nova':
                RocketGraphics.draw_nova_laser(screen, preview_x, preview_y, 40, color)
            elif avatar_type == 'shadow':
                RocketGraphics.draw_shadow_fighter(screen, preview_x, preview_y, 40, color)
            elif avatar_type == 'titan':
                RocketGraphics.draw_titan_cruiser(screen, preview_x, preview_y, 40, color)
            elif avatar_type == 'phoenix':
                RocketGraphics.draw_phoenix_explorer(screen, preview_x, preview_y, 40, color)
            
            # Draw name and description
            name_text = font_large.render(avatar_name, True, color)
            desc_text = font_small.render(avatar_desc, True, color)
            screen.blit(name_text, (150, avatar_y))
            screen.blit(desc_text, (150, avatar_y + 30))
            
            if is_selected:
                selector = font_small.render(">>> SELECTED <<<", True, (0, 255, 255))
                screen.blit(selector, (WIDTH - 280, avatar_y + 15))
            
            avatar_y += 85
        
        pygame.draw.line(screen, (0, 255, 255), (50, HEIGHT - 80), (WIDTH - 50, HEIGHT - 80), 3)
        instruction_text = font_small.render("[ ↑ / ↓ ] Select  |  [ SPACE ] Confirm  |  [ ESC ] Back", True, (200, 200, 200))
        screen.blit(instruction_text, (WIDTH // 2 - 350, HEIGHT - 50))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(AVATARS)
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(AVATARS)
                if event.key == pygame.K_SPACE:
                    return AVATARS[selected][0]
                if event.key == pygame.K_ESCAPE:
                    return None

def show_difficulty_menu():
    """Show difficulty selection"""
    selected = 1  # normal by default
    difficulties = list(DIFFICULTIES.keys())
    
    while True:
        clock.tick(FPS)
        draw_gradient_background(screen)
        draw_starfield(screen)
        
        title = font_menu.render("🎚️ SELECT DIFFICULTY", True, (0, 255, 255))
        screen.blit(title, (WIDTH // 2 - 270, 30))
        
        pygame.draw.line(screen, (0, 255, 255), (50, 110), (WIDTH - 50, 110), 3)
        
        y_offset = 150
        for i, diff in enumerate(difficulties):
            is_selected = i == selected
            diff_data = DIFFICULTIES[diff]
            
            if is_selected:
                pygame.draw.rect(screen, diff_data['color'], (40, y_offset - 5, WIDTH - 80, 80), 3)
                bg_color = tuple(min(int(c * 0.25), 255) for c in diff_data['color'])
                pygame.draw.rect(screen, bg_color, (40, y_offset - 5, WIDTH - 80, 80))
                color = diff_data['color']
            else:
                pygame.draw.rect(screen, (100, 100, 150), (40, y_offset - 5, WIDTH - 80, 80), 1)
                color = (150, 150, 200)
            
            diff_text = font_large.render(diff.upper(), True, color)
            desc_text = font_small.render(diff_data['desc'], True, color)
            
            screen.blit(diff_text, (100, y_offset + 5))
            screen.blit(desc_text, (100, y_offset + 40))
            
            if is_selected:
                selector = font_small.render("★ SELECTED ★", True, color)
                screen.blit(selector, (WIDTH - 250, y_offset + 20))
            
            y_offset += 120
        
        pygame.draw.line(screen, (0, 255, 255), (50, HEIGHT - 80), (WIDTH - 50, HEIGHT - 80), 3)
        instruction = font_small.render("[ ↑ / ↓ ] Select  |  [ SPACE ] Confirm  |  [ ESC ] Back", True, (200, 200, 200))
        screen.blit(instruction, (WIDTH // 2 - 350, HEIGHT - 50))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(difficulties)
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(difficulties)
                if event.key == pygame.K_SPACE:
                    return difficulties[selected]
                if event.key == pygame.K_ESCAPE:
                    return None

def reset_game(avatar_type='falcon', difficulty='normal'):
    """Reset game state"""
    player = Player(avatar_type)
    player.weapon = Weapon()
    player.shield = Shield(max_charge=2)  # Reduced from 3 - absorbs only 2 damage before health taken
    
    # Calculate starting health based on avatar stats
    base_health = 3
    health_bonus = player.stats.get('health_bonus', 0)
    starting_health = max(1, base_health + health_bonus)
    
    # Damage multiplier for this avatar
    player.damage_mult = player.stats.get('damage_mult', 1.0)
    player.weapon.damage = int(1 * player.damage_mult)
    
    # Return tuple with all game state including visual effects systems
    return (player, [], [], [], 0, 0, starting_health, False, 0, 0, [], [], 0, difficulty, None, -100, Achievement(), [], [], ScreenJuice(WIDTH, HEIGHT), ComboVisualizer(WIDTH, HEIGHT))

# Main loop
while True:
    # Main menu
    main_menu_action = show_main_menu()
    if main_menu_action is None:
        break
    
    # Avatar selection
    selected_avatar = show_avatar_selection()
    if selected_avatar is None:
        continue
    
    # Difficulty selection
    current_difficulty = show_difficulty_menu()
    if current_difficulty is None:
        continue
    
    # Game init
    player, enemies, bullets, powerups, spawn_timer, score, health, game_over, combo, max_combo, explosions, floating_texts, screen_shake, difficulty, boss, last_boss_score, achievements, special_effects, visual_effects, screen_juice, combo_visualizer = reset_game(selected_avatar, current_difficulty)
    
    running = True
    boss_spawned_scores = set()
    
    while running:
        clock.tick(FPS)
        
        # Screen shake
        shake_x, shake_y = (random.randint(-3, 3), random.randint(-3, 3)) if screen_shake > 0 else (0, 0)
        if screen_shake > 0:
            screen_shake -= 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                # ESC - return to avatar selection (FIX)
                if event.key == pygame.K_ESCAPE:
                    running = False  # Exit game loop, go back to avatar selection
                    break
                
                if game_over and event.key == pygame.K_r:
                    player, enemies, bullets, powerups, spawn_timer, score, health, game_over, combo, max_combo, explosions, floating_texts, screen_shake, difficulty, boss, last_boss_score, achievements, special_effects, visual_effects, screen_juice, combo_visualizer = reset_game(selected_avatar, current_difficulty)
                    boss_spawned_scores = set()
                
                if not game_over and event.key == pygame.K_SPACE:
                    if player.can_shoot():
                        try:
                            # Handle wizard multi-shot ability
                            if player.stats.get('multi_shot', False):
                                # 3-way shot for wizard/nova
                                bullet_center = Bullet(player.x + player.size // 2, player.y)
                                bullet_left = Bullet(player.x + player.size // 2 - 15, player.y)
                                bullet_right = Bullet(player.x + player.size // 2 + 15, player.y)
                                bullets.extend([bullet_center, bullet_left, bullet_right])
                                # Only show text once when multi-shot is active
                                if not player.multi_shot_text_shown:
                                    floating_texts.append(FloatingText(player.x, player.y - 10, "MULTI-SHOT!", (200, 100, 255), lifetime=30))
                                    player.multi_shot_text_shown = True
                            else:
                                bullet = Bullet(player.x + player.size // 2, player.y)
                                bullets.append(bullet)
                                player.multi_shot_text_shown = False
                            player.shoot()
                        except Exception as e:
                            print(f"Bullet creation error: {e}")
        
        if not game_over:
            # Update player
            keys = pygame.key.get_pressed()
            player.move(keys)
            player.update()
            if hasattr(player, 'shield') and player.shield:
                player.shield.update()
            
            # Update juice effects
            screen_juice.update()
            combo_visualizer.update(combo)
            
            # Difficulty
            difficulty_multiplier = DIFFICULTIES[current_difficulty]
            wave = (score // SPEED_INCREASE_INTERVAL) + 1
            # Cap wave scaling - prevents extreme speeds at high waves
            wave_scaling = min(wave - 1, 12)  # Max 12 wave bonus
            enemy_speed = min(ENEMY_SPEED * difficulty_multiplier['enemy_speed'] + wave_scaling * 0.25, 8.0)  # Cap at 8.0
            spawn_rate = max(MIN_SPAWN_RATE, int(BASE_SPAWN_RATE * difficulty_multiplier['spawn_rate'] - wave_scaling * SPAWN_RATE_DECREASE))
            
            # Spawn enemies
            spawn_timer += 1
            if spawn_timer > spawn_rate:
                new_enemy = create_random_enemy()
                new_enemy.speed = enemy_speed * (1 if new_enemy.enemy_type == 'basic' else (1.8 if new_enemy.enemy_type == 'fast' else 0.5))
                enemies.append(new_enemy)
                spawn_timer = 0
            
            # Boss spawn (FIX - track all spawned boss scores)
            boss_threshold = score - (score % 50)
            if boss_threshold > 0 and boss_threshold not in boss_spawned_scores and boss is None:
                boss = Boss()
                boss_spawned_scores.add(boss_threshold)
            
            # Update boss
            if boss:
                boss.update()
                if boss.off_screen():
                    boss = None
            
            # Update enemies
            for enemy in enemies[:]:
                try:
                    if not enemy:  # Skip None entries
                        if enemy in enemies:
                            enemies.remove(enemy)
                        continue
                    
                    enemy.update()
                    
                    if enemy.off_screen():
                        if enemy in enemies:
                            enemies.remove(enemy)
                        # Updated scoring for all enemy types
                        score_map = {
                            'basic': 1,
                            'fast': 2,
                            'tanky': 3,
                            'spawner': 4,
                            'drone': 1
                        }
                        score_gain = score_map.get(enemy.enemy_type, 1)
                        score += score_gain
                        combo += 1
                        floating_texts.append(FloatingText(enemy.x, enemy.y, f"+{score_gain}", (0, 255, 0), lifetime=40))
                    
                    # Enemy collision with player
                    elif hasattr(player, 'get_rect') and hasattr(enemy, 'get_rect'):
                        try:
                            if player.get_rect().colliderect(enemy.get_rect()):
                                damage = 1
                                if hasattr(player, 'shield') and player.shield:
                                    remaining_damage = player.shield.take_damage(damage)
                                    health -= remaining_damage
                                else:
                                    health -= damage
                                
                                combo = 0
                                screen_shake = 8
                                explosions.append(Explosion(int(player.x + player.size // 2), int(player.y + player.size // 2), (255, 0, 0), 10))
                                if enemy in enemies:
                                    enemies.remove(enemy)
                                
                                if health <= 0:
                                    # Phoenix revive mechanic
                                    if selected_avatar == 'phoenix' and hasattr(player, 'is_mini') and not player.is_mini:
                                        # Revive as mini scout with 3 health
                                        health = 3
                                        player.is_mini = True
                                        player.phoenix_revived = True
                                        # Show revive effect
                                        floating_texts.append(FloatingText(player.x, player.y - 30, "PHOENIX REVIVES!", (255, 100, 50), lifetime=80))
                                        special_effects.append(WaveEffect(int(player.x + player.size // 2), int(player.y + player.size // 2), 300))
                                    else:
                                        game_over = True
                                        max_combo = combo
                                        new_achievements = achievements.check_achievements(score, combo, wave, boss is not None or len(boss_spawned_scores) > 0, max_combo)
                                        save_high_scores(score, max_combo, wave)
                        except Exception as e:
                            print(f"Enemy-player collision error: {e}")
                except Exception as e:
                    print(f"Enemy update error: {e}")
                    if enemy in enemies:
                        enemies.remove(enemy)
            
            # Update bullets
            for bullet in bullets[:]:
                try:
                    if not bullet:  # Skip None entries
                        if bullet in bullets:
                            bullets.remove(bullet)
                        continue
                    
                    bullet.update()
                    
                    if bullet.off_screen():
                        if bullet in bullets:
                            bullets.remove(bullet)
                    else:
                        # Check collision with enemies
                        collision_found = False
                        for enemy in enemies[:]:
                            if not enemy:  # Skip None entries
                                continue
                            try:
                                if hasattr(bullet, 'get_rect') and hasattr(enemy, 'get_rect'):
                                    if bullet.get_rect().colliderect(enemy.get_rect()):
                                        collision_found = True
                                        # Use avatar damage multiplier + combo multiplier
                                        base_damage = int(getattr(player, 'weapon', Weapon()).damage * getattr(player, 'damage_mult', 1.0))
                                        combo_bonus = max(0, (combo // 3)) * 0.1  # +10% per 3 combo
                                        final_damage = int(base_damage * (1.0 + combo_bonus))
                                        is_killed = enemy.take_damage(final_damage)
                                        
                                        if is_killed:
                                            # Professional explosion system
                                            explosions.append(Explosion(int(enemy.x + enemy.size // 2), int(enemy.y + enemy.size // 2), (255, 165, 0), 20))
                                            explosions.append(ParticleExplosion(int(enemy.x + enemy.size // 2), int(enemy.y + enemy.size // 2), (255, 165, 0), 25, 'mixed'))
                                            
                                            special_effects.append(CritHitEffect(int(enemy.x + enemy.size // 2), int(enemy.y + enemy.size // 2)))
                                            special_effects.append(StarburstEffect(int(enemy.x + enemy.size // 2), int(enemy.y + enemy.size // 2), (255, 255, 100), 40))
                                            
                                            # Add visual burst effect
                                            visual_effects.append(EnergyPulse(int(enemy.x + enemy.size // 2), int(enemy.y + enemy.size // 2), 100, (255, 200, 100)))
                                            
                                            # Screen shake feedback
                                            screen_juice.trigger_shake(intensity=3, duration=8)
                                            
                                            if enemy in enemies:
                                                enemies.remove(enemy)
                                            
                                            # Updated scoring map
                                            score_map = {
                                                'basic': 1,
                                                'fast': 2,
                                                'tanky': 3,
                                                'spawner': 4,
                                                'drone': 1
                                            }
                                            score_gained = score_map.get(enemy.enemy_type, 1)
                                            score += score_gained
                                            combo += 1
                                            
                                            # Use advanced ShinyNumber instead of regular floating text
                                            floating_texts.append(ShinyNumber(enemy.x, enemy.y, score_gained, (255, 215, 0)))
                                            
                                            if random.random() < 0.20:  # Increased from 0.15 - 20% chance for powerup
                                                power_type = random.choice(['health', 'fire_rate'])
                                                powerups.append(PowerUp(enemy.x, enemy.y, power_type))
                                                special_effects.append(LootEffect(int(enemy.x), int(enemy.y)))
                                        else:
                                            # Show damage taken with combo bonus indicator
                                            damage_text = f"-{final_damage}"
                                            damage_color = (255, 255, 100) if combo_bonus > 0 else (255, 100, 100)
                                            floating_texts.append(ShinyNumber(enemy.x, enemy.y, final_damage, damage_color))
                                            # Small screen shake for non-kill hits too
                                            screen_juice.trigger_shake(intensity=1.5, duration=4)
                                        
                                        if bullet in bullets:
                                            bullets.remove(bullet)
                                        break
                            except Exception as e:
                                print(f"Bullet-enemy collision error: {e}")
                        
                        # Check collision with boss
                        if not collision_found and boss:
                            try:
                                if hasattr(bullet, 'get_rect') and hasattr(boss, 'get_rect'):
                                    if bullet.get_rect().colliderect(boss.get_rect()):
                                        base_damage = int(getattr(player, 'weapon', Weapon()).damage * getattr(player, 'damage_mult', 1.0))
                                        combo_bonus = max(0, (combo // 3)) * 0.1  # +10% per 3 combo
                                        final_damage = int(base_damage * (1.0 + combo_bonus))
                                        is_killed = boss.take_damage(final_damage)
                                        if bullet in bullets:
                                            bullets.remove(bullet)
                                        
                                        if is_killed:
                                            explosions.append(Explosion(int(boss.x + boss.size // 2), int(boss.y + boss.size // 2), (200, 0, 255), 50))
                                            explosions.append(ParticleExplosion(int(boss.x + boss.size // 2), int(boss.y + boss.size // 2), (200, 100, 255), 50, 'mixed'))
                                            special_effects.append(WaveEffect(int(boss.x + boss.size // 2), int(boss.y + boss.size // 2), 400))
                                            special_effects.append(StarburstEffect(int(boss.x + boss.size // 2), int(boss.y + boss.size // 2), (200, 0, 255), 80))
                                            
                                            # Maximum screen juice for boss kill
                                            visual_effects.append(ScreenFlash((200, 0, 255), duration=15))
                                            visual_effects.append(EnergyPulse(int(boss.x + boss.size // 2), int(boss.y + boss.size // 2), 300, (200, 100, 255)))
                                            
                                            # Intense screen effects
                                            screen_juice.trigger_shake(intensity=10, duration=20)
                                            screen_juice.add_chromatic_aberration(8)
                                            screen_juice.scanline_intensity = 0.8
                                            
                                            score += 100
                                            combo += 10
                                            screen_shake = 30
                                            floating_texts.append(FloatingText(boss.x, boss.y, "BOSS DEFEATED!", (255, 0, 255), lifetime=80))
                                            new_achievements = achievements.check_achievements(score, combo, wave, True, max_combo)
                                            boss = None
                            except Exception as e:
                                print(f"Bullet-boss collision error: {e}")
                except Exception as e:
                    print(f"Bullet update error: {e}")
                    if bullet in bullets:
                        bullets.remove(bullet)
            
            # Boss collision with player
            if boss:
                try:
                    if hasattr(player, 'get_rect') and hasattr(boss, 'get_rect'):
                        if player.get_rect().colliderect(boss.get_rect()):
                            damage = 2
                            if hasattr(player, 'shield') and player.shield:
                                remaining_damage = player.shield.take_damage(damage)
                                health -= remaining_damage
                            else:
                                health -= damage
                            
                            combo = 0
                            screen_shake = 15
                            explosions.append(Explosion(int(player.x + player.size // 2), int(player.y + player.size // 2), (255, 0, 0), 20))
                            
                            if health <= 0:
                                # Phoenix revive mechanic
                                if selected_avatar == 'phoenix' and hasattr(player, 'is_mini') and not player.is_mini:
                                    # Revive as mini scout with 3 health
                                    health = 3
                                    player.is_mini = True
                                    player.phoenix_revived = True
                                    # Show revive effect
                                    floating_texts.append(FloatingText(player.x, player.y - 30, "PHOENIX REVIVES!", (255, 100, 50), lifetime=80))
                                    special_effects.append(WaveEffect(int(player.x + player.size // 2), int(player.y + player.size // 2), 300))
                                else:
                                    game_over = True
                                    max_combo = combo
                                    new_achievements = achievements.check_achievements(score, combo, wave, True, max_combo)
                                    save_high_scores(score, max_combo, wave)
                except Exception as e:
                    print(f"Boss-player collision error: {e}")
            
            # Update power-ups
            for powerup in powerups[:]:
                try:
                    powerup.update()
                    
                    if powerup.off_screen():
                        if powerup in powerups:
                            powerups.remove(powerup)
                    elif player.get_rect().colliderect(powerup.get_rect()):
                        if powerup.power_type == 'health':
                            # Calculate max health for this avatar
                            max_health = 3 + player.stats.get('health_bonus', 0)
                            health = min(health + HEALTH_RESTORE_VALUE, max(1, max_health))
                            floating_texts.append(ShinyNumber(player.x, player.y, 0, (0, 255, 0)))
                            visual_effects.append(ScreenFlash((0, 255, 0), duration=10))
                            # Screen juice for health pickup
                            screen_juice.trigger_shake(intensity=2, duration=6)
                            special_effects.append(StarburstEffect(int(player.x + player.size // 2), int(player.y + player.size // 2), (0, 255, 0), 50))
                        else:
                            player.fire_rate_boost = FIRE_RATE_BOOST_DURATION
                            floating_texts.append(ShinyNumber(player.x, player.y, 0, (255, 255, 0)))
                            visual_effects.append(ScreenFlash((255, 255, 0), duration=10))
                            # Screen juice for boost pickup
                            screen_juice.trigger_shake(intensity=2.5, duration=6)
                            special_effects.append(StarburstEffect(int(player.x + player.size // 2), int(player.y + player.size // 2), (255, 255, 0), 50))
                            screen_juice.add_chromatic_aberration(3)
                        
                        if powerup in powerups:
                            powerups.remove(powerup)
                except Exception as e:
                    print(f"Power-up error: {e}")
                    if powerup in powerups:
                        powerups.remove(powerup)
            
            # Update explosions
            for explosion in explosions[:]:
                try:
                    explosion.update()
                    if explosion.is_done():
                        if explosion in explosions:
                            explosions.remove(explosion)
                except Exception as e:
                    if explosion in explosions:
                        explosions.remove(explosion)
            
            # Update floating text
            for text in floating_texts[:]:
                try:
                    text.update()
                    if not text.is_alive():
                        if text in floating_texts:
                            floating_texts.remove(text)
                except Exception as e:
                    if text in floating_texts:
                        floating_texts.remove(text)
            
            # Update special effects (crits, waves, loot)
            for effect in special_effects[:]:
                try:
                    effect.update()
                    if effect.is_done():
                        if effect in special_effects:
                            special_effects.remove(effect)
                except Exception as e:
                    if effect in special_effects:
                        special_effects.remove(effect)
            
            # Update visual effects (screen flashes, energy pulses, etc)
            for vfx in visual_effects[:]:
                try:
                    vfx.update()
                    if vfx.is_done():
                        if vfx in visual_effects:
                            visual_effects.remove(vfx)
                except Exception as e:
                    if vfx in visual_effects:
                        visual_effects.remove(vfx)
        
        # Draw
        draw_gradient_background(screen)
        draw_starfield(screen)
        
        if not game_over:
            try:
                offset_x, offset_y = shake_x, shake_y
                temp_surface = pygame.Surface((WIDTH, HEIGHT))
                temp_surface.fill((0, 0, 0))
                temp_surface.set_colorkey((0, 0, 0))
                
                # Draw everything on temp surface with error protection
                try:
                    player.draw(temp_surface)
                except Exception as e:
                    print(f"Player draw error: {e}")
                
                for enemy in enemies[:]:
                    try:
                        if enemy:
                            enemy.draw(temp_surface)
                    except Exception as e:
                        print(f"Enemy draw error: {e}")
                
                if boss:
                    try:
                        boss.draw(temp_surface)
                    except Exception as e:
                        print(f"Boss draw error: {e}")
                
                for bullet in bullets[:]:
                    try:
                        if bullet:
                            bullet.draw(temp_surface)
                    except Exception as e:
                        print(f"Bullet draw error: {e}")
                
                for powerup in powerups[:]:
                    try:
                        if powerup:
                            powerup.draw(temp_surface)
                    except Exception as e:
                        print(f"Powerup draw error: {e}")
                
                for explosion in explosions[:]:
                    try:
                        if explosion:
                            explosion.draw(temp_surface)
                    except Exception as e:
                        print(f"Explosion draw error: {e}")
                
                for text in floating_texts[:]:
                    try:
                        if text:
                            text.draw(temp_surface, font_floating)
                    except Exception as e:
                        print(f"Text draw error: {e}")
                
                for effect in special_effects[:]:
                    try:
                        if effect:
                            effect.draw(temp_surface)
                    except Exception as e:
                        print(f"Effect draw error: {e}")
                
                # Draw particle effects (energy pulses, etc) on temp surface
                for vfx in visual_effects[:]:
                    try:
                        if vfx and hasattr(vfx, 'draw') and not hasattr(vfx, '__class__') or vfx.__class__.__name__ not in ['ScreenFlash']:
                            if vfx.__class__.__name__ in ['EnergyPulse', 'ShieldEffect']:
                                vfx.draw(temp_surface)
                    except Exception as e:
                        print(f"Visual effect draw error: {e}")
            except Exception as e:
                log_crash(f"Critical drawing error: {e}")
                print(f"Drawing error: {e}")
            
            screen.blit(temp_surface, (offset_x, offset_y))
            
            # Draw UI with error protection
            try:
                if hasattr(player, 'shield') and player.shield:
                    try:
                        player.shield.draw(screen, player.x, player.y, player.size)
                    except Exception as e:
                        print(f"Shield draw error: {e}")
            except Exception as e:
                print(f"Shield access error: {e}")
            
            # Top info with better styling
            try:
                score_text = font_small.render(f"Score: {score}", True, (0, 255, 100))
                combo_text = font_small.render(f"Combo: {combo}", True, (255, 165, 0) if combo > 0 else (100, 100, 100))
                wave_text = font_small.render(f"Wave: {wave}", True, (0, 200, 255))
                
                # Draw semi-transparent background for info
                pygame.draw.rect(screen, (20, 40, 60), (5, 5, 200, 115), 0)
                pygame.draw.rect(screen, (0, 150, 255), (5, 5, 200, 115), 2)
                
                screen.blit(score_text, (20, 20))
                screen.blit(combo_text, (20, 50))
                screen.blit(wave_text, (20, 80))
                
                # Avatar info with ability (right side with background)
                avatar_display_names = {
                    'falcon': 'Falcon Rocket (Shield)',
                    'nova': 'Nova Laser (Multi-Shot)',
                    'shadow': 'Shadow Fighter (Speed)',
                    'titan': 'Titan Cruiser (Tank)',
                    'phoenix': 'Phoenix Explorer (Revive)'
                }
                avatar_text = font_tiny.render(f"Avatar: {avatar_display_names.get(selected_avatar, 'Falcon')}", True, (100, 200, 255))
                difficulty_text = font_tiny.render(f"Difficulty: {current_difficulty.upper()}", True, DIFFICULTIES[current_difficulty]['color'])
                
                # Draw background for avatar/difficulty info
                pygame.draw.rect(screen, (20, 40, 60), (WIDTH - 290, 5, 285, 75), 0)
                pygame.draw.rect(screen, (0, 150, 255), (WIDTH - 290, 5, 285, 75), 2)
                
                screen.blit(avatar_text, (WIDTH - 280, 15))
                screen.blit(difficulty_text, (WIDTH - 280, 45))
                
                # Calculate actual max health for this avatar
                base_health = 3
                avatar_health_bonus = player.stats.get('health_bonus', 0) if hasattr(player, 'stats') else 0
                max_health_val = max(1, base_health + avatar_health_bonus)
                
                # Mini scout stays at 3 health max
                if hasattr(player, 'is_mini') and player.is_mini:
                    max_health_val = 3
                
                # Health bar
                bar_width = 300
                bar_height = 30
                bar_x = WIDTH // 2 - bar_width // 2
                bar_y = HEIGHT - 50
                
                pygame.draw.rect(screen, (60, 60, 60), (bar_x - 5, bar_y - 5, bar_width + 10, bar_height + 10))
                pygame.draw.rect(screen, (30, 30, 30), (bar_x, bar_y, bar_width, bar_height))
                
                health_ratio = health / max(1, max_health_val)  # Prevent division by zero
                health_color = (255, 0, 0) if health <= 1 else (255, 165, 0) if health <= max_health_val // 2 else (0, 255, 0)
                pygame.draw.rect(screen, health_color, (bar_x, bar_y, int(bar_width * health_ratio), bar_height))
                pygame.draw.rect(screen, (0, 255, 255), (bar_x, bar_y, bar_width, bar_height), 3)
                
                is_mini = hasattr(player, 'is_mini') and player.is_mini
                health_text_display = "SCOUT MODE" if is_mini else f"HEALTH: {health}/{max_health_val}"
                health_text = font_small.render(health_text_display, True, (255, 100, 50) if is_mini else health_color)
                screen.blit(health_text, (bar_x + 80 if is_mini else bar_x + 60, bar_y + 5))
                
                # Draw advanced combo visualizer
                if combo > 0:
                    combo_visualizer.draw_advanced_meter(screen, font_small, font_large)
                
                if hasattr(player, 'fire_rate_boost') and player.fire_rate_boost > 0:
                    boost_progress = player.fire_rate_boost / max(1, FIRE_RATE_BOOST_DURATION)  # Prevent division by zero
                    boost_text = font_small.render(f"FIRE BOOST: {player.fire_rate_boost // 10}s", True, (255, 255, 0))
                    pygame.draw.rect(screen, (60, 60, 0), (WIDTH // 2 - 150, 30, 300, 35), 0)
                    pygame.draw.rect(screen, (255, 255, 0), (WIDTH // 2 - 150, 30, int(300 * boost_progress), 35))
                    pygame.draw.rect(screen, (255, 255, 0), (WIDTH // 2 - 150, 30, 300, 35), 3)
                    screen.blit(boost_text, (WIDTH // 2 - 140, 37))
                
                menu_hint = font_tiny.render("Press ESC to return to menu", True, (150, 150, 150))
                screen.blit(menu_hint, (WIDTH - 280, HEIGHT - 20))
            except Exception as e:
                log_crash(f"UI rendering error: {e}")
                print(f"UI rendering error: {e}")
            
            # Draw screen flash effects (on top of everything)
            try:
                for vfx in visual_effects[:]:
                    try:
                        if vfx and vfx.__class__.__name__ == 'ScreenFlash':
                            vfx.draw(screen)
                    except Exception as e:
                        pass
            except Exception as e:
                pass
            
        
        else:
            # Game Over screen
            high_score, best_combo, best_wave = load_high_scores()
            
            over_text = font_large.render("GAME OVER", True, (255, 100, 100))
            avatar_text = font_large.render(f"{selected_avatar.upper()}", True, (100, 200, 255))
            
            final_score_text = font_small.render(f"Final Score: {score}", True, (0, 255, 100))
            max_combo_text = font_small.render(f"Max Combo: {max_combo}", True, (255, 165, 0))
            wave_text = font_small.render(f"Final Wave: {wave}", True, (0, 200, 255))
            
            is_high_score = score == high_score and score > 0
            high_score_text = font_small.render("★ NEW HIGH SCORE! ★" if is_high_score else f"High Score: {high_score}", True, (255, 215, 0) if is_high_score else (150, 150, 150))
            
            restart_text = font_small.render("[ R ] Restart Game", True, (150, 200, 255))
            menu_text = font_small.render("[ ESC ] Back to Menu", True, (150, 150, 150))
            
            screen.blit(over_text, (WIDTH // 2 - 180, HEIGHT // 2 - 160))
            screen.blit(avatar_text, (WIDTH // 2 - 120, HEIGHT // 2 - 80))
            screen.blit(wave_text, (WIDTH // 2 - 120, HEIGHT // 2))
            screen.blit(final_score_text, (WIDTH // 2 - 120, HEIGHT // 2 + 40))
            screen.blit(max_combo_text, (WIDTH // 2 - 120, HEIGHT // 2 + 80))
            screen.blit(high_score_text, (WIDTH // 2 - 150, HEIGHT // 2 + 130))
            screen.blit(restart_text, (WIDTH // 2 - 130, HEIGHT // 2 + 180))
            screen.blit(menu_text, (WIDTH // 2 - 160, HEIGHT // 2 + 220))
        
        draw_border(screen)
        pygame.display.flip()

pygame.quit()
sys.exit()

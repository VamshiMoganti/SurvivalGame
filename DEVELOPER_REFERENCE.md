# 🎮 DEVELOPER QUICK REFERENCE - System Architecture

## Module Dependencies
```
Main.py (Core Game Loop)
├── story.py (Story & Progression)
│   ├── Campaign phases (4 acts)
│   ├── Story beats (10 narrative moments)
│   ├── Boss data (5 types)
│   └── Milestones (4 achievements)
│
├── boss_enhanced.py (Boss Management)
│   ├── EnhancedBoss class
│   ├── 5 unique boss types
│   ├── Boss factory (create_boss_for_wave)
│   └── Scaled health calculation
│
├── ui_advanced.py (Professional UI)
│   ├── AdvancedUIRenderer (Gameplay HUD)
│   ├── MenuRenderer (Menu UI)
│   ├── Story text display
│   └── Phase/objective tracking
│
├── screen_juice.py (Visual Effects)
│   └── Professional visual feedback
│
└── Other modules
    ├── player.py
    ├── enemy.py
    ├── bullet.py
    ├── powerup.py
    ├── particle.py
    ├── visual_effects.py
    ├── sprites.py
    ├── space_graphics.py
    └── settings.py
```

## Game State Tuple (Reset Every Game)
```python
(
    player,              # Player object
    enemies,             # List of enemy objects
    bullets,             # List of bullet objects
    powerups,            # List of powerup objects
    spawn_timer,         # Enemy spawn counter
    score,               # Current score
    health,              # Current health
    game_over,           # Boolean game state
    combo,               # Current combo counter
    max_combo,           # Best combo in session
    explosions,          # Particle explosions
    floating_texts,      # Damage/score numbers
    screen_shake,        # Screen shake duration
    difficulty,          # Selected difficulty
    boss,                # Current boss or None
    last_boss_score,     # Last boss spawn score
    achievements,        # Achievement tracker
    special_effects,     # Special effect list
    visual_effects,      # Visual effects (flashes, pulses)
    screen_juice,        # Screen effects manager
    combo_visualizer,    # Advanced combo display
    story_system,        # Story & progression (NEW)
    ui_renderer          # Advanced UI system (NEW)
)
```

## Key Game Constants

### Waves & Progression
| Component | Value | Notes |
|-----------|-------|-------|
| SPEED_INCREASE_INTERVAL | 10 | Points per wave |
| MAX_WAVE_SCALING | 12 | Cap on difficulty bonus |
| MAX_ENEMY_SPEED | 8.0 | Speed hard limit |
| MIN_SPAWN_RATE | 15 | Minimum frames between spawns |

### Boss System
| Component | Value | Notes |
|-----------|-------|-------|
| Boss Waves | [5, 8, 10, 12, 15, 16, 18, 20] | Strategic spawn points |
| Destroyer Health | 30 base | Wave-scaled |
| Interceptor Health | 25 base | Wave-scaled |
| Commander Health | 45 base | Wave-scaled |
| Apex Health | 50 base | Wave-scaled |
| Mothership Health | 150 base | Heavily wave-scaled |

### Health Bar
| Component | Value | Changed |
|-----------|-------|---------|
| HEALTH_DEPLETION_SPEED | 3.0 | 3x FASTER (was 1.0) |

## New Classes

### StorySystem (story.py)
```python
class StorySystem:
    def __init__(self)
    def update(wave, score, combo, boss_defeated)  # Call every frame
    def next_story_text()  # Get queued story text
    def get_phase_name(wave=None)  # Get phase name
    def get_phase_objectives(wave=None)  # Get objectives
    def is_milestone_wave(wave)  # Check if milestone
```

### EnhancedBoss (boss_enhanced.py)
```python
class EnhancedBoss:
    def __init__(x, y, wave, boss_type='destroyer', difficulty=1.0)
    def update()  # Call every frame
    def take_damage(damage) -> bool  # Returns True if killed
    def off_screen() -> bool
    def get_rect() -> pygame.Rect
    def draw(surface)
    def get_display_name() -> str
    def get_difficulty_rating() -> int  # Star rating
```

### AdvancedUIRenderer (ui_advanced.py)
```python
class AdvancedUIRenderer:
    def __init__(width, height)
    def render_hud(screen, player, wave, score, combo, health, max_health,
                   avatar_type, difficulty)  # Main render call
    def add_story_text(text, color, duration)
    def show_milestone(text, reward)
```

## Boss Spawning Logic

```python
# Boss waves trigger one time each
BOSS_WAVES = [5, 8, 10, 12, 15, 16, 18, 20]

# Spawn conditions:
if wave in BOSS_WAVES and boss is None and wave not in boss_spawned_scores:
    boss = create_boss_for_wave(wave)
    boss_spawned_scores.add(wave)  # Prevent respawn
```

## Story Integration Points

### Phase Auto-Detection
```python
phase_id, phase_data = get_current_phase(wave)
# Returns current phase ID and phase data dictionary
```

### Story Beats
```python
story_beat = get_story_beat(wave)
# Returns beat data if this wave has a story moment
# Otherwise returns None
```

### Milestone Detection
```python
milestone_text, reward = ui_renderer.show_milestone(wave)
# Called during boss kill to show achievement
```

## Performance Notes

### Optimizations Made:
- Boss spawning is one-time per wave (no spam)
- Health bar update is faster (3x multiplier)
- UI rendering is consolidated into single renderer
- Story text queued (not shown all at once)
- Effects properly cleaned up

### Potential Improvements:
- Could cache moon rendered UI elements
- Could batch story text rendering
- Could use object pools for bosses
- Could optimize boss collision detection

## Common Issues & Solutions

### Boss doesn't spawn?
- Check wave is in BOSS_WAVES list
- Verify boss is None before spawn
- Check boss_spawned_scores tracking

### Story text not showing?
- Call ui_renderer.add_story_text(text, color, duration)
- Ensure story_system.update() called every frame
- Check display queue isn't full

### UI misaligned?
- Check WIDTH and HEIGHT constants
- Verify font sizes are reasonable
- Test on different screen sizes

### Boss health wrong?
- Use get_boss_health(wave, difficulty) function
- Verify phase multipliers are correct
- Check wave scaling is applied

## Testing Checklist

- [ ] Game boots without errors
- [ ] Avatar selection works
- [ ] Difficulty selection works
- [ ] Story text appears on new phase
- [ ] Boss appears at wave 5
- [ ] Boss health scales with waves
- [ ] Boss dies and score increases
- [ ] Next boss appears at wave 8
- [ ] Milestone shows at wave 5
- [ ] UI displays correctly
- [ ] Health bar updates quickly
- [ ] Game reaches wave 20
- [ ] Mothership appears
- [ ] Mothership dies = victory
- [ ] Game handles loss correctly
- [ ] All 5 boss types spawn
- [ ] Smooth 60 FPS
- [ ] No crashes

## Quick Command Reference

### Start Game
```bash
python main.py
```

### Test Imports
```bash
python -c "from story import StorySystem; print('OK')"
python -c "from boss_enhanced import EnhancedBoss; print('OK')"
python -c "from ui_advanced import AdvancedUIRenderer; print('OK')"
```

### Syntax Check
```bash
python -m py_compile main.py
```

---

## 🎮 The New System In Action

**Old Flow:**
```
Game Loop → Boss random spawn → Instant kill → Repeat infinitely
```

**New Flow:**
```
Game Loop
  ├→ Story System Update (tracks progression)
  ├→ Check if current wave has story beat
  ├→ Check if current wave should spawn boss
  ├→ If yes: Create EnhancedBoss with scaled health
  ├→ Update UI with phase objectives
  ├→ Render advanced HUD showing all info
  ├→ Display story text when phase changes
  ├→ Show milestone when boss dies at key wave
  └→ Continue to next phase or victory
```

**Result:** Meaningful, story-driven experience with clear progression!

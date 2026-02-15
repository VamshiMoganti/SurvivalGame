# Screen settings
WIDTH = 800
HEIGHT = 600
FPS = 60

# Player settings
PLAYER_SIZE = 50
PLAYER_SPEED = 5
PLAYER_COOLDOWN = 15  # Frames between shots

# Enemy settings
ENEMY_SIZE = 50
ENEMY_SPEED = 5
BASE_SPAWN_RATE = 60  # Frames between spawns
MIN_SPAWN_RATE = 15   # Minimum spawn rate

# Difficulty scaling
SPEED_INCREASE_INTERVAL = 10  # Increase wave every 10 points (gentler progression)
SPAWN_RATE_DECREASE = 1.5    # Decrease spawn rate more gradually

# Difficulty settings (moved from main.py)
DIFFICULTIES = {
    'easy': {'spawn_rate': 1.3, 'enemy_speed': 0.6, 'color': (0, 200, 0), 'desc': 'Perfect for beginners'},
    'normal': {'spawn_rate': 1.0, 'enemy_speed': 0.85, 'color': (100, 200, 255), 'desc': 'Balanced experience'},
    'hard': {'spawn_rate': 0.65, 'enemy_speed': 1.0, 'color': (255, 165, 0), 'desc': 'For experienced players'},
    'nightmare': {'spawn_rate': 0.4, 'enemy_speed': 1.2, 'color': (255, 0, 0), 'desc': 'Insane difficulty'}
}

# Power-up settings
POWERUP_SIZE = 30
POWERUP_SPEED = 3
HEALTH_RESTORE_VALUE = 1
FIRE_RATE_BOOST_DURATION = 300  # Frames

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)

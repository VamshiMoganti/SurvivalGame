"""
🎮 STORY & PROGRESSION SYSTEM - Survival Game Adventure
Complete narrative-driven game with story beats, progression, achievements
"""

# Campaign Phases - Story Arc
CAMPAIGN_PHASES = {
    1: {
        'name': 'ESCAPE THE ASTEROID FIELD',
        'description': 'Survive the chaos of the asteroid field',
        'waves': (1, 5),
        'story_intro': 'Your ship has crashed in an asteroid field!\nSurvive the incoming asteroids and escape!',
        'objectives': ['Destroy 50 asteroids', 'Survive 5 waves', 'Build your combo to 10'],
        'difficulty_mult': 1.0,
        'boss_waves': [5],
        'rewards': 'Unlocked: Fire Rate Upgrade',
    },
    2: {
        'name': 'ENEMY OUTPOST DETECTED',
        'description': 'An enemy military base appears in your path',
        'waves': (6, 10),
        'story_intro': 'An enemy outpost has been detected!\nThey\'re sending waves of fighters to destroy you!',
        'objectives': ['Destroy 100 enemy fighters', 'Survive waves 6-10', 'Reach a 20 combo streak'],
        'difficulty_mult': 1.3,
        'boss_waves': [8, 10],
        'rewards': 'Unlocked: Shield Generator',
    },
    3: {
        'name': 'THE HUNTER SQUADRON',
        'description': 'Elite hunter squadrons closing in',
        'waves': (11, 15),
        'story_intro': 'The enemy has sent their elite hunter squadron!\nThese fighters are fast and deadly!',
        'objectives': ['Destroy 150 hunters', 'Survive waves 11-15', 'Get maximum combos'],
        'difficulty_mult': 1.6,
        'boss_waves': [12, 15],
        'rewards': 'Unlocked: Damage Boost',
    },
    4: {
        'name': 'THE MOTHERSHIP ARRIVES',
        'description': 'The enemy mothership has finally appeared',
        'waves': (16, 20),
        'story_intro': 'The massive enemy mothership is here!\nThis is what we\'ve been training for!\nDefeat the mothership and save the sector!',
        'objectives': ['Survive mothership waves', 'Destroy the mothership', 'Complete the story'],
        'difficulty_mult': 2.0,
        'boss_waves': [16, 18, 20],
        'boss_health_multiplier': 2.5,
        'rewards': 'VICTORY! Saved the sector!',
    },
}

# Story beats - events that trigger during gameplay
STORY_BEATS = {
    1: {
        'wave': 1,
        'text': 'Enemy contact! Incoming asteroids!',
        'color': (255, 100, 0),
    },
    2: {
        'wave': 5,
        'text': 'First boss approaching! It\'s a command destroyer!',
        'color': (255, 0, 0),
    },
    3: {
        'wave': 6,
        'text': 'We\'ve reached the outpost perimeter. More enemies incoming!',
        'color': (255, 165, 0),
    },
    4: {
        'wave': 8,
        'text': 'Elite hunters engaged! These are dangerous opponents!',
        'color': (255, 50, 50),
    },
    5: {
        'wave': 10,
        'text': 'The outpost commander ship is here! Massive battle incoming!',
        'color': (255, 0, 0),
    },
    6: {
        'wave': 11,
        'text': 'Hunter squadron detected! We\'re in their territory now!',
        'color': (255, 100, 50),
    },
    7: {
        'wave': 15,
        'text': 'The hunters are retreating... Something bigger is coming!',
        'color': (200, 50, 200),
    },
    8: {
        'wave': 16,
        'text': 'IT\'S HERE! THE MOTHERSHIP! ALL HANDS TO BATTLE STATIONS!',
        'color': (255, 0, 0),
    },
    9: {
        'wave': 18,
        'text': 'The mothership is weakening! One more push!',
        'color': (255, 200, 0),
    },
    10: {
        'wave': 20,
        'text': 'FINAL STRIKE! Destroy the core!',
        'color': (0, 255, 100),
    },
}

def get_current_phase(wave):
    """Get the story phase for a given wave"""
    for phase_id, phase_data in CAMPAIGN_PHASES.items():
        wave_min, wave_max = phase_data['waves']
        if wave_min <= wave <= wave_max:
            return phase_id, phase_data
    return 4, CAMPAIGN_PHASES[4]  # Default to final phase

def get_story_beat(wave):
    """Get story beat for current wave"""
    for beat_id, beat_data in STORY_BEATS.items():
        if beat_data['wave'] == wave:
            return beat_data
    return None

def get_phase_progress(wave):
    """Get progress through current phase as percentage"""
    phase_id, phase_data = get_current_phase(wave)
    wave_min, wave_max = phase_data['waves']
    progress = ((wave - wave_min) / (wave_max - wave_min + 1)) * 100
    return min(100, max(0, progress))

# Avatar abilities - Unique mechanics for each
AVATAR_ABILITIES = {
    'falcon': {
        'name': 'Falcon Rocket',
        'title': 'Shield Master',
        'ability': 'Reinforced Shield System',
        'description': 'Can absorb more damage with advanced shield technology',
        'special_perk': '+2 Shield Health',
        'stat_bonuses': {
            'health_bonus': 1,
            'shield_bonus': 1,
        },
        'unique_effect': 'shield_regeneration',
        'color': (0, 150, 255),
    },
    'nova': {
        'name': 'Nova Laser',
        'title': 'Weapons Expert',
        'ability': 'Multi-Shot Laser System',
        'description': 'Fires 3 devastating laser blasts simultaneously',
        'special_perk': 'Triple Fire Power',
        'stat_bonuses': {
            'damage_mult': 1.5,
            'multi_shot': True,
        },
        'unique_effect': 'multi_shot_enabled',
        'color': (255, 200, 0),
    },
    'shadow': {
        'name': 'Shadow Fighter',
        'title': 'Speed Demon',
        'ability': 'Hyperdrive Engines',
        'description': 'Extreme speed and agility - quick reflexes save lives',
        'special_perk': '+2 Speed',
        'stat_bonuses': {
            'speed_mult': 1.8,
            'fire_rate_bonus': 1.2,
        },
        'unique_effect': 'speed_boosted',
        'color': (150, 0, 200),
    },
    'titan': {
        'name': 'Titan Cruiser',
        'title': 'Tank Commander',
        'ability': 'Armor Plating System',
        'description': 'Heavily armored with reinforced hull - takes half damage',
        'special_perk': 'Damage Reduction 50%',
        'stat_bonuses': {
            'health_bonus': 2,
            'damage_reduction': 0.5,
        },
        'unique_effect': 'damage_reduction',
        'color': (200, 100, 0),
    },
    'phoenix': {
        'name': 'Phoenix Explorer',
        'title': 'Revival Master',
        'ability': 'Phoenix Protocol Resurrection',
        'description': 'Can revive as a scout ship after taking fatal damage',
        'special_perk': 'One Life Revive',
        'stat_bonuses': {
            'revive_enabled': True,
        },
        'unique_effect': 'phoenix_revival',
        'color': (255, 100, 0),
    },
}

# Boss types with unique personalities
BOSS_TYPES = {
    'destroyer': {
        'name': 'Command Destroyer',
        'health_base': 30,
        'description': 'Heavy weapons platform',
        'difficulty': 1,
        'color': (200, 0, 0),
        'rarity': 'common',
    },
    'interceptor': {
        'name': 'Hunter Interceptor',
        'health_base': 25,
        'description': 'Fast and evasive',
        'difficulty': 1.5,
        'color': (255, 100, 0),
        'rarity': 'uncommon',
    },
    'commander': {
        'name': 'Outpost Commander',
        'health_base': 45,
        'description': 'Elite military vessel',
        'difficulty': 2,
        'color': (255, 0, 100),
        'rarity': 'rare',
    },
    'apex': {
        'name': 'Apex Hunter',
        'health_base': 50,
        'description': 'Deadliest hunter in the squadron',
        'difficulty': 2.5,
        'color': (200, 50, 200),
        'rarity': 'epic',
    },
    'mothership': {
        'name': 'Enemy Mothership',
        'health_base': 150,
        'description': 'Massive space fortress',
        'difficulty': 4,
        'color': (255, 0, 0),
        'rarity': 'legendary',
    },
}

# Milestone achievements
MILESTONES = {
    1: {'wave': 5, 'text': 'First Boss Defeat! 🎊', 'reward': 50},
    2: {'wave': 10, 'text': 'Cleared Outpost! 🏆', 'reward': 100},
    3: {'wave': 15, 'text': 'Defeated Hunter Squadron! ⭐', 'reward': 150},
    4: {'wave': 20, 'text': 'SAVED THE SECTOR! 🌟', 'reward': 500},
}

def get_boss_type_for_wave(wave):
    """Determine which boss type appears at a given wave"""
    if wave == 5:
        return 'destroyer'
    elif wave == 8:
        return 'interceptor'
    elif wave == 10:
        return 'commander'
    elif wave == 12:
        return 'interceptor'
    elif wave == 15:
        return 'apex'
    elif wave == 16:
        return 'mothership'
    elif wave == 18:
        return 'mothership'
    elif wave == 20:
        return 'mothership'
    else:
        # Random mini-boss at other waves
        types = ['destroyer', 'interceptor', 'commander']
        import random
        return random.choice(types)

def get_boss_health(wave, base_difficulty=1.0):
    """Calculate boss health for a given wave"""
    boss_type = get_boss_type_for_wave(wave)
    boss_data = BOSS_TYPES[boss_type]
    base_health = boss_data['health_base']
    
    # Health scales with wave
    wave_multiplier = 1.0 + (wave - 1) * 0.1
    
    # Apply difficulty
    phase_id, phase_data = get_current_phase(wave)
    difficulty_mult = phase_data.get('boss_health_multiplier', 1.0)
    
    return int(base_health * wave_multiplier * difficulty_mult * base_difficulty)

class StorySystem:
    """Manages story progression and narrative"""
    
    def __init__(self):
        self.current_phase = 1
        self.current_phase_data = CAMPAIGN_PHASES[1]
        self.story_text_queue = []
        self.displayed_beats = set()
        self.completed_phases = []
        self.total_progress = 0  # Overall campaign progress 0-100
    
    def update(self, wave, score, combo, boss_defeated):
        """Update story based on game progress"""
        # Update current phase
        phase_id, phase_data = get_current_phase(wave)
        if phase_id != self.current_phase:
            self.current_phase = phase_id
            self.current_phase_data = phase_data
            self.story_text_queue.append({
                'text': f"=== {phase_data['name'].upper()} ===\n{phase_data['story_intro']}",
                'duration': 200,
                'color': (0, 255, 150),
                'size': 'large',
            })
        
        # Check for story beats
        beat = get_story_beat(wave)
        if beat and wave not in self.displayed_beats:
            self.displayed_beats.add(wave)
            self.story_text_queue.append({
                'text': beat['text'],
                'duration': 120,
                'color': beat['color'],
                'size': 'medium',
            })
        
        # Update overall progress
        self.total_progress = min(100, (wave / 20) * 100)
    
    def get_phase_name(self, wave=None):
        """Get name of current or specified phase"""
        if wave is None:
            return self.current_phase_data['name']
        phase_id, phase_data = get_current_phase(wave)
        return phase_data['name']
    
    def get_phase_objectives(self, wave=None):
        """Get objectives for current phase"""
        if wave is None:
            return self.current_phase_data.get('objectives', [])
        phase_id, phase_data = get_current_phase(wave)
        return phase_data.get('objectives', [])
    
    def next_story_text(self):
        """Get next story text to display"""
        if self.story_text_queue:
            return self.story_text_queue.pop(0)
        return None
    
    def is_milestone_wave(self, wave):
        """Check if this wave is a story milestone"""
        for milestone_id, milestone_data in MILESTONES.items():
            if milestone_data['wave'] == wave:
                return True
        return False
    
    def get_milestone_text(self, wave):
        """Get milestone text for wave"""
        for milestone_id, milestone_data in MILESTONES.items():
            if milestone_data['wave'] == wave:
                return milestone_data['text'], milestone_data['reward']
        return None, 0

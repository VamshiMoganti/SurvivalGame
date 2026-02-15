import json
import os

SCORES_FILE = "highscores.json"

def load_high_scores():
    """Load high scores from file"""
    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, 'r') as f:
                data = json.load(f)
                return data.get('high_score', 0), data.get('best_combo', 0), data.get('best_wave', 0)
        except:
            return 0, 0, 0
    return 0, 0, 0

def save_high_scores(score, combo, wave):
    """Save high scores to file"""
    try:
        existing = {}
        if os.path.exists(SCORES_FILE):
            with open(SCORES_FILE, 'r') as f:
                existing = json.load(f)
        
        existing['high_score'] = max(existing.get('high_score', 0), score)
        existing['best_combo'] = max(existing.get('best_combo', 0), combo)
        existing['best_wave'] = max(existing.get('best_wave', 0), wave)
        
        with open(SCORES_FILE, 'w') as f:
            json.dump(existing, f)
    except:
        pass

def get_high_scores():
    """Get all high scores"""
    return load_high_scores()

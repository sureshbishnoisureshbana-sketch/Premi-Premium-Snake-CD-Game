# Game Configuration

import os
from constants import *

class GameConfig:
    """Game configuration settings"""
    
    # Display Settings
    SCREEN_WIDTH = SCREEN_WIDTH
    SCREEN_HEIGHT = SCREEN_HEIGHT
    GRID_SIZE = GRID_SIZE
    FPS = 60
    WINDOW_TITLE = "🐍 Premi Premium Snake CD Game"
    
    # Game Settings
    INITIAL_SNAKE_LENGTH = 3
    STARTING_DIFFICULTY = DIFFICULTY_MEDIUM
    STARTING_MODE = MODE_CLASSIC
    
    # Audio Settings
    SOUND_ENABLED = True
    MUSIC_ENABLED = True
    SOUND_VOLUME = 0.7
    MUSIC_VOLUME = 0.5
    
    # Graphics Settings
    SHOW_GRID = True
    SMOOTH_ANIMATION = True
    PARTICLE_EFFECTS = True
    GLOW_EFFECT = True
    
    # Difficulty Speeds
    SPEEDS = {
        DIFFICULTY_EASY: SPEED_EASY,
        DIFFICULTY_MEDIUM: SPEED_MEDIUM,
        DIFFICULTY_HARD: SPEED_HARD,
        DIFFICULTY_EXTREME: SPEED_EXTREME
    }
    
    # Score Multipliers by Difficulty
    SCORE_MULTIPLIERS = {
        DIFFICULTY_EASY: 1.0,
        DIFFICULTY_MEDIUM: 1.5,
        DIFFICULTY_HARD: 2.0,
        DIFFICULTY_EXTREME: 3.0
    }
    
    # Colors Theme
    THEME = {
        'background': COLOR_DARK_BLUE,
        'snake_head': COLOR_GREEN,
        'snake_body': COLOR_DARK_GREEN,
        'food': COLOR_RED,
        'obstacle': COLOR_ORANGE,
        'text': COLOR_WHITE,
        'grid': COLOR_GRAY,
        'border': COLOR_LIGHT_GRAY
    }
    
    # Highscore File
    HIGHSCORE_FILE = "highscore.txt"
    
    @staticmethod
    def load_config():
        """Load configuration"""
        return GameConfig()

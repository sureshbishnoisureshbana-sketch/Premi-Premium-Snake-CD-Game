# Food Class

import pygame
import random
from constants import *

class Food:
    """Food entity that snake eats"""
    
    def __init__(self, width, height):
        """Initialize food at random position"""
        self.width = width
        self.height = height
        self.x = random.randint(0, width - 1)
        self.y = random.randint(0, height - 1)
        self.value = SCORE_FOOD
    
    def spawn_random(self, snake_body=None, obstacles=None):
        """Spawn food at random position (avoid snake and obstacles)"""
        while True:
            self.x = random.randint(0, self.width - 1)
            self.y = random.randint(0, self.height - 1)
            
            # Check if position is valid
            if (self.x, self.y) not in (snake_body or []):
                if obstacles is None or (self.x, self.y) not in obstacles:
                    break
    
    def get_position(self):
        """Get food position"""
        return (self.x, self.y)
    
    def draw(self, surface, grid_size):
        """Draw food on surface"""
        x = self.x * grid_size
        y = self.y * grid_size
        
        # Draw outer circle (glow)
        center = (x + grid_size // 2, y + grid_size // 2)
        pygame.draw.circle(surface, COLOR_ORANGE, center, grid_size // 2 + 2, 2)
        
        # Draw main food
        pygame.draw.circle(surface, COLOR_RED, center, grid_size // 2)
        
        # Draw shine/highlight
        shine_center = (x + grid_size // 3, y + grid_size // 3)
        pygame.draw.circle(surface, COLOR_YELLOW, shine_center, 3)
    
    def is_eaten(self, snake_head):
        """Check if snake ate this food"""
        return snake_head == (self.x, self.y)

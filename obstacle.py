# Obstacle Class

import pygame
import random
from constants import *

class Obstacle:
    """Obstacles that snake must avoid"""
    
    def __init__(self, width, height):
        """Initialize obstacles list"""
        self.width = width
        self.height = height
        self.obstacles = []
    
    def add_obstacle(self, x, y):
        """Add an obstacle at position"""
        if 0 <= x < self.width and 0 <= y < self.height:
            if (x, y) not in self.obstacles:
                self.obstacles.append((x, y))
    
    def remove_obstacle(self, x, y):
        """Remove an obstacle"""
        if (x, y) in self.obstacles:
            self.obstacles.remove((x, y))
    
    def spawn_random_obstacles(self, count, snake_body=None, food_pos=None):
        """Spawn random obstacles"""
        self.obstacles = []
        attempts = 0
        max_attempts = count * 10
        
        while len(self.obstacles) < count and attempts < max_attempts:
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)
            
            # Check if position is valid
            if (x, y) not in (snake_body or []) and (x, y) != food_pos:
                self.add_obstacle(x, y)
            
            attempts += 1
    
    def create_walls(self):
        """Create border walls"""
        self.obstacles = []
        # Top and bottom walls
        for x in range(self.width):
            self.add_obstacle(x, 0)
            self.add_obstacle(x, self.height - 1)
        # Left and right walls
        for y in range(self.height):
            self.add_obstacle(0, y)
            self.add_obstacle(self.width - 1, y)
    
    def check_collision(self, position):
        """Check if position collides with obstacle"""
        return position in self.obstacles
    
    def get_obstacles(self):
        """Get all obstacles"""
        return self.obstacles
    
    def clear(self):
        """Clear all obstacles"""
        self.obstacles = []
    
    def draw(self, surface, grid_size):
        """Draw obstacles on surface"""
        for obs_x, obs_y in self.obstacles:
            x = obs_x * grid_size
            y = obs_y * grid_size
            rect = pygame.Rect(x, y, grid_size, grid_size)
            
            # Draw obstacle with pattern
            pygame.draw.rect(surface, COLOR_ORANGE, rect)
            pygame.draw.rect(surface, COLOR_RED, rect, 2)
            
            # Draw cross pattern
            pygame.draw.line(surface, COLOR_RED, (x, y), (x + grid_size, y + grid_size), 1)
            pygame.draw.line(surface, COLOR_RED, (x + grid_size, y), (x, y + grid_size), 1)

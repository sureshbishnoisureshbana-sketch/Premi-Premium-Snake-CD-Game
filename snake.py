# Snake Class

import pygame
from constants import *
from collections import deque

class Snake:
    """Snake entity with movement and collision logic"""
    
    def __init__(self, x, y):
        """Initialize snake at starting position"""
        self.body = deque()
        self.direction = (1, 0)  # Moving right initially
        self.next_direction = (1, 0)
        self.grow_pending = 0
        
        # Initialize snake body (3 segments)
        for i in range(2, -1, -1):
            self.body.append((x - i, y))
    
    def move(self):
        """Move snake in current direction"""
        # Update direction
        self.direction = self.next_direction
        
        # Get current head position
        head_x, head_y = self.body[0]
        
        # Calculate new head position
        new_x = head_x + self.direction[0]
        new_y = head_y + self.direction[1]
        
        # Add new head
        self.body.appendleft((new_x, new_y))
        
        # Remove tail if not growing
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()
    
    def grow(self, amount=1):
        """Make snake grow"""
        self.grow_pending += amount
    
    def set_direction(self, direction):
        """Set next direction (prevent 180 degree turns)"""
        # Prevent reversing into itself
        opposite = (-self.direction[0], -self.direction[1])
        if direction != opposite:
            self.next_direction = direction
    
    def get_head(self):
        """Get head position"""
        return self.body[0]
    
    def get_body(self):
        """Get entire body"""
        return list(self.body)
    
    def check_self_collision(self):
        """Check if snake collides with itself"""
        head = self.body[0]
        return head in list(self.body)[1:]
    
    def check_wall_collision(self, width, height):
        """Check if snake collides with walls"""
        head_x, head_y = self.body[0]
        return head_x < 0 or head_x >= width or head_y < 0 or head_y >= height
    
    def get_length(self):
        """Get snake length"""
        return len(self.body)
    
    def reset(self, x, y):
        """Reset snake to starting state"""
        self.body = deque()
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.grow_pending = 0
        
        for i in range(2, -1, -1):
            self.body.append((x - i, y))
    
    def draw(self, surface, grid_size, theme):
        """Draw snake on surface"""
        snake_body = list(self.body)
        
        # Draw body
        for i, segment in enumerate(snake_body[1:]):
            x = segment[0] * grid_size
            y = segment[1] * grid_size
            rect = pygame.Rect(x, y, grid_size, grid_size)
            pygame.draw.rect(surface, theme['snake_body'], rect)
            pygame.draw.rect(surface, COLOR_DARK_GREEN, rect, 2)
        
        # Draw head with glow
        if snake_body:
            head_x, head_y = snake_body[0]
            x = head_x * grid_size
            y = head_y * grid_size
            
            # Draw glow effect
            glow_rect = pygame.Rect(x - 2, y - 2, grid_size + 4, grid_size + 4)
            pygame.draw.ellipse(surface, COLOR_YELLOW, glow_rect, 1)
            
            # Draw head
            rect = pygame.Rect(x, y, grid_size, grid_size)
            pygame.draw.rect(surface, theme['snake_head'], rect)
            pygame.draw.rect(surface, COLOR_YELLOW, rect, 3)
            
            # Draw eyes
            if self.direction == (1, 0):  # Moving right
                eye1 = (x + 12, y + 6)
                eye2 = (x + 12, y + 14)
            elif self.direction == (-1, 0):  # Moving left
                eye1 = (x + 8, y + 6)
                eye2 = (x + 8, y + 14)
            elif self.direction == (0, 1):  # Moving down
                eye1 = (x + 6, y + 12)
                eye2 = (x + 14, y + 12)
            else:  # Moving up
                eye1 = (x + 6, y + 8)
                eye2 = (x + 14, y + 8)
            
            pygame.draw.circle(surface, COLOR_BLACK, eye1, 2)
            pygame.draw.circle(surface, COLOR_BLACK, eye2, 2)

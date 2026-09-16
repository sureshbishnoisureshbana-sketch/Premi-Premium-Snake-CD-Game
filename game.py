# Main Game Logic

import pygame
import sys
import time
from constants import *
from config import GameConfig
from snake import Snake
from food import Food
from obstacle import Obstacle

class GameEngine:
    """Main game engine"""
    
    def __init__(self):
        """Initialize game engine"""
        pygame.init()
        self.config = GameConfig.load_config()
        
        # Screen setup
        self.screen = pygame.display.set_mode((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
        pygame.display.set_caption(self.config.WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        
        # Font setup
        try:
            self.font_large = pygame.font.Font(None, 60)
            self.font_medium = pygame.font.Font(None, 40)
            self.font_small = pygame.font.Font(None, 25)
        except:
            self.font_large = pygame.font.Font(None, 60)
            self.font_medium = pygame.font.Font(None, 40)
            self.font_small = pygame.font.Font(None, 25)
        
        # Game variables
        self.grid_width = self.config.SCREEN_WIDTH // GRID_SIZE
        self.grid_height = self.config.SCREEN_HEIGHT // GRID_SIZE
        
        self.state = GAME_STATE_MENU
        self.difficulty = self.config.STARTING_DIFFICULTY
        self.game_mode = self.config.STARTING_MODE
        self.speed = self.config.SPEEDS[self.difficulty]
        
        # Game objects
        self.snake = None
        self.food = None
        self.obstacles = None
        
        # Game stats
        self.score = 0
        self.high_score = self.load_high_score()
        self.game_over = False
        self.paused = False
        self.frame_count = 0
        self.time_elapsed = 0
        self.start_time = time.time()
        
        self.init_game()
    
    def init_game(self):
        """Initialize new game"""
        self.snake = Snake(self.grid_width // 2, self.grid_height // 2)
        self.food = Food(self.grid_width, self.grid_height)
        self.food.spawn_random(self.snake.get_body())
        
        self.obstacles = Obstacle(self.grid_width, self.grid_height)
        
        if self.game_mode == MODE_SURVIVAL:
            self.obstacles.spawn_random_obstacles(5, self.snake.get_body(), self.food.get_position())
        
        self.score = 0
        self.game_over = False
        self.paused = False
        self.frame_count = 0
        self.time_elapsed = 0
        self.start_time = time.time()
    
    def handle_input(self):
        """Handle user input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                
                if self.state == GAME_STATE_MENU:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                        self.select_difficulty(event.key)
                    if event.key in [pygame.K_c, pygame.K_s, pygame.K_t, pygame.K_e]:
                        self.select_mode(event.key)
                
                elif self.state == GAME_STATE_PLAYING:
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.snake.set_direction((0, -1))
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.snake.set_direction((0, 1))
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.snake.set_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.snake.set_direction((1, 0))
                
                elif self.state == GAME_STATE_GAME_OVER:
                    if event.key == pygame.K_r:
                        self.init_game()
                        self.state = GAME_STATE_PLAYING
                    elif event.key == pygame.K_m:
                        self.state = GAME_STATE_MENU
        
        return True
    
    def select_difficulty(self, key):
        """Select game difficulty"""
        difficulty_map = {
            pygame.K_1: DIFFICULTY_EASY,
            pygame.K_2: DIFFICULTY_MEDIUM,
            pygame.K_3: DIFFICULTY_HARD,
            pygame.K_4: DIFFICULTY_EXTREME
        }
        self.difficulty = difficulty_map.get(key, DIFFICULTY_MEDIUM)
        self.speed = self.config.SPEEDS[self.difficulty]
    
    def select_mode(self, key):
        """Select game mode"""
        mode_map = {
            pygame.K_c: MODE_CLASSIC,
            pygame.K_s: MODE_SURVIVAL,
            pygame.K_t: MODE_TIME_ATTACK,
            pygame.K_e: MODE_ENDLESS
        }
        self.game_mode = mode_map.get(key, MODE_CLASSIC)
        self.init_game()
        self.state = GAME_STATE_PLAYING
    
    def update(self):
        """Update game state"""
        if self.state != GAME_STATE_PLAYING or self.paused:
            return
        
        self.frame_count += 1
        self.time_elapsed = time.time() - self.start_time
        
        # Move snake
        if self.frame_count % (60 // self.speed) == 0:
            self.snake.move()
            self.frame_count = 0
        
        # Check collisions
        head = self.snake.get_head()
        
        # Wall collision
        if self.snake.check_wall_collision(self.grid_width, self.grid_height):
            self.end_game()
            return
        
        # Self collision
        if self.snake.check_self_collision():
            self.end_game()
            return
        
        # Obstacle collision
        if self.obstacles.check_collision(head):
            self.end_game()
            return
        
        # Food collision
        if self.food.is_eaten(head):
            self.score += int(SCORE_FOOD * self.config.SCORE_MULTIPLIERS[self.difficulty])
            self.snake.grow(1)
            self.food.spawn_random(self.snake.get_body(), self.obstacles.get_obstacles())
            
            # Add obstacles in survival mode
            if self.game_mode == MODE_SURVIVAL and self.snake.get_length() % 5 == 0:
                self.obstacles.spawn_random_obstacles(1, self.snake.get_body(), self.food.get_position())
        
        # Time attack mode check
        if self.game_mode == MODE_TIME_ATTACK and self.time_elapsed > TIME_ATTACK_DURATION:
            self.end_game()
    
    def end_game(self):
        """End the game"""
        self.state = GAME_STATE_GAME_OVER
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
    
    def draw(self):
        """Draw game screen"""
        self.screen.fill(self.config.THEME['background'])
        
        if self.state == GAME_STATE_MENU:
            self.draw_menu()
        elif self.state == GAME_STATE_PLAYING:
            self.draw_game()
        elif self.state == GAME_STATE_GAME_OVER:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def draw_menu(self):
        """Draw main menu"""
        # Title
        title = self.font_large.render("🐍 PREMI PREMIUM SNAKE", True, COLOR_GREEN)
        self.screen.blit(title, (self.config.SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
        
        # Difficulty Selection
        diff_text = self.font_medium.render("Select Difficulty:", True, COLOR_YELLOW)
        self.screen.blit(diff_text, (50, 150))
        
        difficulties = [
            ("1 - EASY", COLOR_GREEN),
            ("2 - MEDIUM", COLOR_YELLOW),
            ("3 - HARD", COLOR_ORANGE),
            ("4 - EXTREME", COLOR_RED)
        ]
        
        for i, (text, color) in enumerate(difficulties):
            rendered = self.font_small.render(text, True, color)
            self.screen.blit(rendered, (100, 200 + i * 50))
        
        # Mode Selection
        mode_text = self.font_medium.render("Select Mode:", True, COLOR_YELLOW)
        self.screen.blit(mode_text, (self.config.SCREEN_WIDTH // 2 + 50, 150))
        
        modes = [
            ("C - CLASSIC", COLOR_CYAN),
            ("S - SURVIVAL", COLOR_ORANGE),
            ("T - TIME ATTACK", COLOR_RED),
            ("E - ENDLESS", COLOR_PURPLE)
        ]
        
        for i, (text, color) in enumerate(modes):
            rendered = self.font_small.render(text, True, color)
            self.screen.blit(rendered, (self.config.SCREEN_WIDTH // 2 + 100, 200 + i * 50))
        
        # High Score
        high_score_text = self.font_small.render(f"High Score: {self.high_score}", True, COLOR_CYAN)
        self.screen.blit(high_score_text, (self.config.SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, 600))
    
    def draw_game(self):
        """Draw game screen"""
        # Draw game objects
        self.obstacles.draw(self.screen, GRID_SIZE)
        self.food.draw(self.screen, GRID_SIZE)
        self.snake.draw(self.screen, GRID_SIZE, self.config.THEME)
        
        # Draw UI
        score_text = self.font_small.render(f"Score: {self.score}", True, COLOR_WHITE)
        self.screen.blit(score_text, (10, 10))
        
        high_score_text = self.font_small.render(f"High: {self.high_score}", True, COLOR_CYAN)
        self.screen.blit(high_score_text, (self.config.SCREEN_WIDTH - 250, 10))
        
        mode_text = self.font_small.render(f"Mode: {self.game_mode.upper()}", True, COLOR_YELLOW)
        self.screen.blit(mode_text, (10, 40))
        
        length_text = self.font_small.render(f"Length: {self.snake.get_length()}", True, COLOR_GREEN)
        self.screen.blit(length_text, (self.config.SCREEN_WIDTH - 250, 40))
        
        if self.game_mode == MODE_TIME_ATTACK:
            time_left = max(0, TIME_ATTACK_DURATION - int(self.time_elapsed))
            time_text = self.font_small.render(f"Time: {time_left}s", True, COLOR_RED)
            self.screen.blit(time_text, (self.config.SCREEN_WIDTH // 2 - 50, 10))
        
        if self.paused:
            pause_text = self.font_medium.render("PAUSED", True, COLOR_YELLOW)
            self.screen.blit(pause_text, (self.config.SCREEN_WIDTH // 2 - pause_text.get_width() // 2, 300))
    
    def draw_game_over(self):
        """Draw game over screen"""
        # Draw game in background
        self.obstacles.draw(self.screen, GRID_SIZE)
        self.food.draw(self.screen, GRID_SIZE)
        self.snake.draw(self.screen, GRID_SIZE, self.config.THEME)
        
        # Dark overlay
        overlay = pygame.Surface((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(COLOR_BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game Over Text
        game_over_text = self.font_large.render("GAME OVER!", True, COLOR_RED)
        self.screen.blit(game_over_text, (self.config.SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 150))
        
        # Score
        score_text = self.font_medium.render(f"Final Score: {self.score}", True, COLOR_YELLOW)
        self.screen.blit(score_text, (self.config.SCREEN_WIDTH // 2 - score_text.get_width() // 2, 280))
        
        # High Score
        if self.score == self.high_score and self.score > 0:
            new_high_text = self.font_medium.render("NEW HIGH SCORE!", True, COLOR_GREEN)
            self.screen.blit(new_high_text, (self.config.SCREEN_WIDTH // 2 - new_high_text.get_width() // 2, 350))
        else:
            high_text = self.font_small.render(f"High Score: {self.high_score}", True, COLOR_CYAN)
            self.screen.blit(high_text, (self.config.SCREEN_WIDTH // 2 - high_text.get_width() // 2, 350))
        
        # Instructions
        restart_text = self.font_small.render("Press R to Restart or M for Menu", True, COLOR_WHITE)
        self.screen.blit(restart_text, (self.config.SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 500))
    
    def load_high_score(self):
        """Load high score from file"""
        try:
            with open(self.config.HIGHSCORE_FILE, 'r') as f:
                return int(f.read())
        except:
            return 0
    
    def save_high_score(self):
        """Save high score to file"""
        try:
            with open(self.config.HIGHSCORE_FILE, 'w') as f:
                f.write(str(self.high_score))
        except:
            pass
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            running = self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(self.config.FPS)
        
        self.save_high_score()
        pygame.quit()
        sys.exit()

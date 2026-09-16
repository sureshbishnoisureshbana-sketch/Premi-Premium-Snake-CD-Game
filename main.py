#!/usr/bin/env python3
# Premi Premium Snake CD Game - Main Entry Point

import sys
import os

try:
    import pygame
except ImportError:
    print("\n" + "="*50)
    print("❌ Pygame not installed!")
    print("="*50)
    print("\nPlease install required dependencies:")
    print("  pip install -r requirements.txt")
    print("\nOR install manually:")
    print("  pip install pygame")
    print("="*50 + "\n")
    sys.exit(1)

from game import GameEngine
from constants import *

def print_welcome():
    """Print welcome message"""
    print("\n" + "="*60)
    print("  🐍 Welcome to PREMI PREMIUM SNAKE CD GAME 🐍")
    print("="*60)
    print("\n📋 How to Play:")
    print("  ⬆️  Use Arrow Keys or WASD to move the snake")
    print("  🍎 Eat the red food to grow and earn points")
    print("  ⚠️  Avoid obstacles, walls, and yourself")
    print("  ⏸️  Press SPACE to pause/resume")
    print("  🔄 Press R to restart after game over")
    print("  🏠 Press M to return to menu")
    print("\n🎮 Game Modes:")
    print("  • CLASSIC: Traditional snake gameplay")
    print("  • SURVIVAL: Obstacles appear as you grow")
    print("  • TIME ATTACK: Complete objectives in 60 seconds")
    print("  • ENDLESS: Play as long as you can")
    print("\n⚡ Difficulty Levels:")
    print("  • EASY: Slow and relaxing")
    print("  • MEDIUM: Balanced gameplay")
    print("  • HARD: Challenging speed")
    print("  • EXTREME: Maximum difficulty")
    print("\n" + "="*60)
    print("Starting game...\n")

def main():
    """Main entry point"""
    print_welcome()
    
    try:
        game = GameEngine()
        game.run()
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

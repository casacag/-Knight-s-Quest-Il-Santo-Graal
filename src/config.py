"""
Configurazioni globali per Knight's Quest: Il Santo Graal
"""
from typing import Tuple
import pygame

# Dimensioni schermo
SCREEN_WIDTH: int = 1024
SCREEN_HEIGHT: int = 768
FPS: int = 60

# Colori (RGB)
BLACK: Tuple[int, int, int] = (0, 0, 0)
WHITE: Tuple[int, int, int] = (255, 255, 255)
RED: Tuple[int, int, int] = (255, 0, 0)
GREEN: Tuple[int, int, int] = (0, 255, 0)
BLUE: Tuple[int, int, int] = (0, 0, 255)
BROWN: Tuple[int, int, int] = (139, 69, 19)
GRAY: Tuple[int, int, int] = (128, 128, 128)
GOLD: Tuple[int, int, int] = (255, 215, 0)
SILVER: Tuple[int, int, int] = (192, 192, 192)

# Player settings (ingrandito per miglior visibilità)
PLAYER_WIDTH: int = 64
PLAYER_HEIGHT: int = 80
PLAYER_SPEED: int = 5
PLAYER_JUMP_SPEED: int = -15
PLAYER_MAX_HEALTH: int = 100

# Physics
GRAVITY: int = 1
GROUND_Y: int = SCREEN_HEIGHT - 100

# Input keys
KEY_LEFT: int = pygame.K_LEFT
KEY_RIGHT: int = pygame.K_RIGHT
KEY_JUMP: int = pygame.K_SPACE
KEY_ATTACK: int = pygame.K_x
KEY_QUIT: int = pygame.K_ESCAPE

# Game states
GAME_STATE_MENU: str = "menu"
GAME_STATE_PLAYING: str = "playing"
GAME_STATE_PAUSED: str = "paused"
GAME_STATE_GAME_OVER: str = "game_over"
GAME_STATE_VICTORY: str = "victory"
GAME_STATE_LEVEL_INTRO: str = "level_intro"
GAME_STATE_LEVEL_COMPLETE: str = "level_complete"
GAME_STATE_LEVEL_FAILED: str = "level_failed"

# Levels
LEVEL_1: str = "foresta_maledetta"
LEVEL_2: str = "miniere_argento"
LEVEL_3: str = "caverna_serpente"

# Resources
RESOURCE_GOLD: str = "oro"
RESOURCE_SILVER: str = "argento"
RESOURCE_MYRRH: str = "mirra"

# Collectibles settings (ingrandite per miglior visibilità)
COLLECTIBLE_SIZE = 32  # Raddoppiato da 16 a 32
GOLD_VALUE = 10
SILVER_VALUE = 25
MYRRH_VALUE = 50

# Collectible spawn settings
MAX_COLLECTIBLES = 8
SPAWN_CHANCE_GOLD = 0.7
SPAWN_CHANCE_SILVER = 0.25
SPAWN_CHANCE_MYRRH = 0.05

# Collectible effects
GOLD_HEAL_AMOUNT = 5
SILVER_HEAL_AMOUNT = 15
MYRRH_HEAL_AMOUNT = 30 

# Combat system settings (Bilanciato per gameplay strategico)
PLAYER_ATTACK_DAMAGE = 25
DEMON_HP = 75                    # 3 colpi del player per uccidere (25 x 3 = 75)
DEMON_ATTACK_DAMAGE = 10         # 10 colpi per uccidere il player (100 HP / 10 = 10 damage)
BOSS_HP = 250                    # 10 colpi del player per uccidere (25 x 10 = 250)
BOSS_ATTACK_DAMAGE = 20          # 5 colpi per uccidere il player (100 HP / 5 = 20 damage)
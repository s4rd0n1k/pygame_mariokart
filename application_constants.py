import pygame
pygame.font.init()
TESTING = False
MOVE_SCALER = 7
BALANCED_MAXSPEED = 3
BALANCED_RATE = 0.35
BALANACED_MAXSPEED_SLOW = 1
BALANCED_RATE_SLOW = 0.2
BALANCED_MAXROT = 0.6
BALANCED_RATEROT = 0.1
BALANCED_RESISTANCE = 0.1
BALANCED_RESISTANCE_SLOW = 0.2

IMAGE_FOLDER = 'sprites/'
SCREEN_DIMENSIONS = WIDTH, HEIGHT = 700, 560

GAME_FONT = 'segoe ui'
FONT_SMALL = pygame.font.SysFont(GAME_FONT, 10)
FONT_STANDARD = pygame.font.SysFont(GAME_FONT, 20)
FONT_BIG = pygame.font.SysFont(GAME_FONT, 50)

BLACK = pygame.Color(0, 0, 0, 255)
WHITE = pygame.Color(255, 255, 255, 255)
YELLOW = pygame.Color(255, 255, 0, 255)
GOLD = pygame.Color(240, 240, 10)
WATER = pygame.Color(0, 38, 255, 255)
LAVA = pygame.Color(255, 255, 255, 255)
TRACK_BROWN = pygame.Color(81, 49, 26, 255)
TRACK_GRAY = pygame.Color(63, 63, 63, 255)
DOT_M = pygame.Color(249, 0, 0, 255)
DOT_P = pygame.Color(249, 107, 107, 255)
DOT_B = pygame.Color(248, 183, 0, 255)
DOT_L = pygame.Color(0, 248, 0, 255)
KEYSET_DEFAULT = (pygame.K_UP, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_SPACE)

ns = pygame.Surface((32, 32))
ns.fill(BLACK)
ns_text = FONT_SMALL.render('no sprite image :(', False, WHITE)
ns.blit(ns_text, (5, 5))
del ns_text
NOSPRITE = ns.copy()
del ns

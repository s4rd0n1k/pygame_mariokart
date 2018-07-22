import pygame
import io
import re

class Map():
    def __init__(self, map_img, signal_img, laps, checks, karts, powerups):
        self.image = map_img
        self.signal = signal_img
        self.laps = laps
        self.checkpoints = checks
        self.kart_spawns = karts
        self.powerup_spawns = powerups
    def print(self):
        print('MAP DATA:')
        print('laps: ' + str(self.laps))
        print('checkpoints: ' + str(self.checkpoints))
        print('kart spawnpoints: ' + str(self.kart_spawns))
        print('powerup spawnpoints: ' + str(self.powerup_spawns))

def load_Map(filename):
    filename += '.txt'
    #load plaintext of file
    with open(filename, 'r') as f:
        map_data = f.read()
    print(map_data)
    #regex text into map name, signal name, laps, checkpoints, kart spawns, powerup spawns
    img_file = re.search(r'(?<=m:).*(?=,)', map_data).group(0)
    signal_file = re.search(r'(?<=s:).*(?=,)', map_data).group(0)
    laps = re.search(r'(?<=l:).*(?=,)', map_data).group(0)
    checks = re.search(r'(?<=c:).*(?=,)', map_data).group(0)
    karts = re.search(r'(?<=k:).*(?=,)', map_data).group(0)
    powerups = re.search(r'(?<=p:).*(?=,)', map_data).group(0)
    
    checks = re.split(';', checks)
    karts = re.split(';', karts)
    powerups = re.split(';', powerups)
    #load map image, signal image
    map_img = pygame.image.load(img_file).convert_alpha()
    signal_img = pygame.image.load(signal_file).convert_alpha()
    #build Map object from data
    return Map(map_img, signal_img, laps, checks, karts, powerups)

pygame.init()
screen = pygame.display.set_mode((400, 400))
gamemap = load_Map('sprites\map_01')
gamemap.print()
screen.blit(gamemap.image, (0, 0))
screen.blit(gamemap.signal, (0, 0))
pygame.display.flip()

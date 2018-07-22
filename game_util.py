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
        self.print_map()
    def print_map(self):
        print('MAP DATA:')
        print('laps: ' + str(self.laps))
        print('checkpoints: ' + str(self.checkpoints))
        print('kart spawnpoints: ' + str(self.kart_spawns))
        print('powerup spawnpoints: ' + str(self.powerup_spawns))

def load_Map(filename):
    print(filename)
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
    
    checks_str = re.split(';', checks)
    karts_str = re.split(';', karts)
    powerups_str = re.split(';', powerups)
    print(checks_str)
    #casting text from map into usable int values
    checks = []
    karts = []
    powerups = []
    
    for i in range(0, len(checks_str)):
        check_str = checks_str[i].split('-')
        check_ints = (int(check_str[0]), int(check_str[1]), int(check_str[2]))
        checks.append(check_ints)
    for i in range(0, len(karts_str)):
        kart_str = karts_str[i].split('-')
        kart_ints = (int(kart_str[0]), int(kart_str[1]), int(kart_str[2]))
        karts.append(kart_ints)
    for i in range(0, len(powerups_str)):
        powerup_str = powerups_str[i].split('-')
        powerup_ints= (int(powerup_str[0]), int(powerup_str[1]), int(powerup_str[2]))
        powerups.append(powerup_ints)

    laps = int(laps)
    #load map image, signal image
    map_img = pygame.image.load(img_file).convert_alpha()
    signal_img = pygame.image.load(signal_file).convert_alpha()
    #build Map object from data
    return Map(map_img, signal_img, laps, checks, karts, powerups)

#placeholder for file based maps
#map1 = Map(pygame.image.load('sprites/map_01.png').convert_alpha(),
#           pygame.image.load('sprites/mapsignal_01.png').convert_alpha(),
#           ((5620, 780), (5620, 820), (5580, 780), (5580, 820)), 90,
#           ((5600, 2400), (2400, 2400), (2400, 4000), (3200, 1600)),
#           (5700, 800),
#           0)
#maptest = Map(pygame.image.load('sprites/map_test1.png').convert_alpha(),
#           pygame.image.load('sprites/mapsignal_test1.png').convert_alpha(),
#           ((2000, 3600), (2050, 3600), (2000, 3650), (2050, 3650)), 0,
#           None,
#           None,
#           1)

#iterate through 12 32x32 images, dependent on symmetric rotation
animation_kart = (32, 32), 15, 'r-s'
animation_checkpoint = 'r'

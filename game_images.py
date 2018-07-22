import pygame
import application_constants as game

ui_images = dict()
game_images = dict()

def li(path):
    return pygame.image.load(game.IMAGE_FOLDER + path).convert_alpha()

def safe_load_game():
    global game_images
    if not game_images:
        load_game_images()
    
def load_game_images():
    global ui_images
    game_images['mario'] = li('mario.png')
    game_images['peach'] = li('peach.png')
    game_images['bowser'] = li('bowser.png')
    game_images['luigi'] = li('luigi.png')
    game_images['checkpoint'] = li('checkpoint.png')
    game_images['finish'] = li('finish.png')
    game_images['powerup_box'] = li('powerup_box.png')
    game_images['trap_banana'] = li('trap_banana.png')
    game_images['trap_shell_f'] = li('trap_shell_f.png')
    game_images['trap_shell_b'] = li('trap_shell_b.png')

def get_game_images():
    global game_images
    safe_load_game()
    return game_images

def get_game_image(image_name):
    global game_images
    safe_load_game()
    return game_images[image_name]

def safe_load_ui():
    global ui_images
    if not ui_images:
        load_ui_images()
    
def load_ui_images():
    global ui_images
    ui_images['menu_background'] = li('menu_background.png')
    ui_images['win_background'] = li('win_background.png')
    
    ui_images['logo'] = li('logo.png')
    ui_images['logo_big'] = li('logo_big.png')
    
    ui_images['minimap_1'] = li('minimap_1.png')
    ui_images['minimap_2'] = li('minimap_2.png')
    ui_images['minimap_3'] = li('minimap_3.png')
    
    ui_images['button_1p'] = li('button_1p.png')
    ui_images['button_2p'] = li('button_2p.png')
    ui_images['button_3p'] = li('button_3p.png')
    ui_images['button_quit'] = li('button_quit.png')
    ui_images['button_map1'] = li('button_map1.png')
    ui_images['button_map2'] = li('button_map2.png')
    ui_images['button_map3'] = li('button_map3.png')
    ui_images['button_start'] = li('button_start.png')
    ui_images['button_start_inactive'] = li('button_start_inactive.png')
    ui_images['button_back'] = li('button_back.png')
    ui_images['button_playagain'] = li('button_playagain.png')
    ui_images['button_stats'] = li('button_stats.png')
    
    ui_images['img_podium'] = li('img_podium.png')
    

def get_ui_images():
    global ui_images
    safe_load_ui()
    return ui_images

def get_ui_image(image_name):
    global ui_images
    safe_load_ui()
    return ui_images[image_name]
    

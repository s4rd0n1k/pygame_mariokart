import sys, math, random, time, traceback
import pygame
import camera
MENU_DIMENSIONS = WIDTH, HEIGHT = 700, 560
SCREEN_DIMENSIONS = None
pygame.init()
game = None
entity = None
UI = None
animations = None

random.seed()

screen = pygame.display.set_mode(MENU_DIMENSIONS)
load_screen = pygame.image.load('sprites/logo.png')
menu_background = None
#UI groups
playermenu = pygame.sprite.Group()
mapmenu = pygame.sprite.Group()
gamemenu = pygame.sprite.Group()
winmenu = pygame.sprite.Group()
#game groups
live_entities = pygame.sprite.Group()
karts = pygame.sprite.Group()
cameras = []
winners = []
map_img = None
signal_img = None
#winscreen groups
podium_karts = pygame.sprite.Group()

selected_map = None
countdown = 3
mode_time = time.time()
fps = 0
gamemode = 0
players = 1
#30 updates per second
pacing = 10
update_timer = 0
powerup_respawn = 32
powerup_timer = 0

readytoload = False

def get_karts():
    global karts
    return karts

def current_ui():
    #returns the current UI
    global gamemode
    if gamemode == 0:
        return playermenu
    elif gamemode == 1:
        return mapmenu
    elif gamemode == 2:
        return gamemenu
    elif gamemode == 3:
        return winmenu

def set_gamemode(value):
    #safe assignment of gamemode
    global gamemode, mode_time
    if value == '-':
        gamemode -= 1
        return
    gamemode = value
    mode_time = time.time()
    print('* gamemode = ', gamemode)

def exit_game(state, error = None):
    print('exiting game with state ', str(state))
    pygame.quit()
    if error: raise error
    sys.exit()

def select_players():
    #display the player selection UI
    set_gamemode(0)

def set_players(value):
    #assigns values for an n-player game
    global players
    players = value
    print('* players = ', players)
    select_map()

def select_map():
    #display the map selection UI
    set_gamemode(1)

def set_map(map_number):
    #records map choice
    global readytoload, selected_map
    readytoload = True
    mapmenu.sprites()[1].set_image(image_name = 'button_start')
    #todo: add more maps
    selected_map = 'sprites/map_'
    selected_map += str(map_number)
    print('* map = ', map_number)
    pass

def loadscreen():
    #quickly displays a load screen
    screen = pygame.display.set_mode(MENU_DIMENSIONS)
    screen.fill((0, 0, 0))
    screen.blit(load_screen, ((WIDTH-load_screen.get_width())/2, (HEIGHT-load_screen.get_height())/2)) 
    pygame.display.update()

def load_game():
    #prepares
    global readytoload
    if not readytoload:
        return
    loadscreen()
    loadSprites_game01()
    set_gamemode(2)

def win_game01(winners):
    loadSprites_win(winners)
    set_gamemode(3)

def unload_game01():
    loadscreen()
    global live_entities, karts, podium_karts, cameras, winners, players
    live_entities = pygame.sprite.Group()
    karts = pygame.sprite.Group()
    podium_karts = pygame.sprite.Group()
    cameras = []
    winners = []
    players = 0
    set_gamemode(0)
    
def loadSprites_win(winners):
    import game_util
    print("< loading win screen")
    background = UI.Element(image_name = 'win_background')
    podium = UI.Element(image_name = 'img_podium', centered = True)
    button_playagain = UI.Button(image_name = 'button_playagain', pos = (0, 90), centered = True,
                                 onclick = unload_game01)
    button_quit = UI.Button(image_name = 'button_quit', pos = (0, 180), centered = True,
                            onclick = exit_game, arg = 1)
    #to be implemented
    button_stats = UI.Button(image_name = 'button_stats', pos = (0, 130), centered = True)
    
    for i in range(0, players):
        if i > 2:
            break
        if i == 0:
            p = (WIDTH/2, HEIGHT/2 - (podium.rect.height/2))
        elif i == 1:
            p = (WIDTH/2 - 92, HEIGHT/2 - 10 - (podium.rect.height*(1/8)))
        elif i == 2:
            p = (WIDTH/2 + 92, HEIGHT/2 - 10 + (podium.rect.height*(1/8)))
        kart = entity.Entity(image_name = winners[i], animation = game_util.animation_kart,
                             pos = p)
        podium_karts.add(kart)

    winmenu.add(background, podium, button_playagain, button_quit, button_stats)
    screen = pygame.display.set_mode(MENU_DIMENSIONS)
    print("> loaded win screen")
    
def loadSprites_game01():
    #loading images & instantiating sprites for game01
    print("< loading game")
    global entity, live_entities, gamemap, map_img, signal_img, SCREEN_DIMENSIONS, selected_map
    import game_entity
    import game_util
    entity = game_entity
    
    #map class placeholder
    print(selected_map)
    gamemap = game_util.load_Map(selected_map)
    map_img = gamemap.image
    signal_img = gamemap.signal
    print('- loaded maps')
    
    #karts
    for i in range(0, players):
        pos_data = gamemap.kart_spawns[i]
        posi = (pos_data[0], pos_data[1])
        rot = pos_data[2]
        if i == 0:
            kart = entity.Kart(pygame.K_w, pygame.K_d, pygame.K_a, pygame.K_e, image_name = 'mario',
                               pos = posi, rotation = rot,
                               animation = game_util.animation_kart)
        elif i == 1:
            kart = entity.Kart(pygame.K_i, pygame.K_l, pygame.K_j, pygame.K_o, image_name = 'peach',
                               pos = posi, rotation = rot,
                               animation = game_util.animation_kart)
        elif i == 2:
            kart = entity.Kart(pygame.K_UP, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_0, image_name = 'bowser',
                               pos = posi, rotation = rot,
                               animation = game_util.animation_kart)
        else:
            kart = entity.Kart(pygame.K_z, pygame.K_x, pygame.K_c, pygame.K_v, image_name = 'luigi',
                               pos = posi, rotation = rot,
                               animation = game_util.animation_kart)
        karts.add(kart)
    print('- loaded karts')
    
    #checkpoints and finish
    chs = gamemap.checkpoints
    for i in range(1, len(chs)):
        check_data = chs[i]
        check = entity.Checkpoint(stage = i-1, image_name = 'checkpoint',
                                  pos = (check_data[0], check_data[1]), rotation = check_data[2],
                                  animation = game_util.animation_checkpoint)
        live_entities.add(check)
    check_data = chs[0]
    finish = entity.Checkpoint(stage = len(chs)-1, image_name = 'finish',
                               pos = (check_data[0], check_data[1]), rotation = check_data[2],
                               animation = game_util.animation_checkpoint)
    live_entities.add(finish)
    print('- loaded checkpoints')
    
    #cameras
    for i in range(0, players):
        #create a new camera, displaying in an appropriate section of the screen, centered around a kart
        newcam = camera.Camera(WIDTH * i, HEIGHT * i, WIDTH, HEIGHT, karts.sprites()[i], 0, 0, map_img.get_width(), map_img.get_height())
        cameras.append(newcam)
    print('- loaded cameras')

    spawn_powerups()
    print('- loaded powerups')
    
    live_entities.add(karts.sprites())
    
    SCREEN_DIMENSIONS = WIDTH * players, HEIGHT
    screen = pygame.display.set_mode(SCREEN_DIMENSIONS)
    print("> loaded game")

def loadSprites_menu():
    #loading images & instantiating sprites for UI
    print("< loading UI")
    global menu_background, UI, game, MENU_DIMENSIONS, WIDTH, HEIGHT
    import game_ui
    import application_constants
    UI = game_ui
    game = application_constants
    MENU_DIMENSIONS = WIDTH, HEIGHT = game.SCREEN_DIMENSIONS
    menu_background = UI.ui_images['menu_background']
    
    #buttons
    one_player = UI.Button(image_name = 'button_1p', pos = (0, -30), centered = True, onclick = set_players, arg = 1)
    two_player = UI.Button(image_name = 'button_2p', pos = (0, 10), centered = True, onclick = set_players, arg = 2)
    three_player = UI.Button(image_name = 'button_3p', pos =  (0, 50), centered = True, onclick = set_players, arg = 3)
    quit_game = UI.Button(image_name = 'button_quit', pos = (0, 110), centered = True, onclick = exit_game, arg = 1)

    select_map_one = UI.Button(image_name = 'button_map1', pos = (75, 440), onclick = set_map, arg = 1)
    select_map_two = UI.Button(image_name = 'button_map2', pos = (275, 440), onclick = set_map, arg = 2)
    select_map_three = UI.Button(image_name = 'button_map2', pos = (475, 440), onclick = set_map, arg = 3)
    play = UI.Button(image_name = 'button_start_inactive', pos = (0, -30), centered = True, onclick = load_game)
    back = UI.Button(image_name = 'button_back', pos = (0, 255), centered = True, onclick = set_gamemode, arg = '-')

    #images
    logo = UI.Element(pos = (0, -150), image_name='logo_big', centered = True)
    map_backdrop = pygame.Surface((154, 154))
    map_backdrop.fill(game.BLACK)
    map_selected = map_backdrop.copy()
    map_selected.fill(game.YELLOW)
    map_one_bg = UI.Element(pos = (73, 278), image=map_backdrop)
    map_two_bg = UI.Element(pos = (273, 278), image=map_backdrop)
    map_three_bg = UI.Element(pos = (473, 278), image=map_backdrop)
    map_one = UI.Element(pos = (75, 280), image_name='minimap_1')
    map_two = UI.Element(pos = (275, 280), image_name='minimap_1')
    map_three = UI.Element(pos = (475, 280), image_name='minimap_1')

    playermenu.add(logo, one_player, two_player, three_player, quit_game)
    mapmenu.add(logo, play, back, map_one_bg, map_two_bg, map_three_bg, map_one, map_two, map_three, select_map_one, select_map_two, select_map_three)
    print("> loaded UI")

def get_input(kart, keys):
    #binds input to kart control functions
    kart.set_accel(0)
    kart.set_turn(0)
    if keys[kart.ACCEL]:
        kart.set_accel(1)
    if keys[kart.TURN_RIGHT]:
        kart.set_turn(1)
    if keys[kart.TURN_LEFT]:
        kart.set_turn(-1)
    if keys[kart.USE]:
        kart.use_item()
    if keys[pygame.K_1]:
        kart.powerup = 'shroom'
    if keys[pygame.K_2]:
        kart.powerup = 'banana'
    if keys[pygame.K_3]:
        kart.powerup = 'shell_f'
    if keys[pygame.K_4]:
        kart.powerup = 'shell_b'
def spawn_powerups():
    #populate the map with powerup boxes
    spawnpoints = gamemap.powerup_spawns
    for point in spawnpoints:
        p1 = (point[0] + 70, point[1] - 70)
        p2 = point
        p3 = (point[0] - 70, point[1] + 70)
        types = []
        for i in range(0, 3):
            n = random.randint(0, 4)
            if n < 2:
                types.append('shroom')
            elif n == 2:
                types.append('banana')
            elif n == 3:
                types.append('shell_b')
            elif n == 4:
                types.append('shell_f')
        box1 = entity.Powerup(pu_type = types[0], pos = p1)
        box2 = entity.Powerup(pu_type = types[1], pos = p2)
        box3 = entity.Powerup(pu_type = types[2], pos = p3)
        live_entities.add(box1, box2, box3)

def update(gamemode):
    #game logic
    global update_timer, powerup_timer
    global pacing, powerup_respawn
    global fps
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game(0)
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                clicked = [button for button in current_ui() if button.rect.collidepoint(pos)]
                for button in clicked:
                    try:
                        button.clicked()
                    except AttributeError:
                        print('that\'s not a button!')
        if gamemode == 2:
            #pacing
            if update_timer > 0:
                update_timer -= 1
                return
            update_timer = round(fps / 45)
            if (time.time() - powerup_timer) > powerup_respawn:
                powerup_timer = time.time()
                spawn_powerups()
            #gameplay
            if len(winners) >= players:
                win_game01(winners)
                print(winners)
            for i in range(0, len(cameras)):
                cam = cameras[i]
                active_rect = cam.rect()
                active_entities = active_rect.collidelistall(
                    [sprite.rect() for sprite in live_entities.sprites()])
                
                #countdown timing
                if time.time() - mode_time < countdown:
                    cam.update()
                    return
            
                for n in active_entities:
                    entity = live_entities.sprites()[n]
                    if not entity.alive and not entity.updated:
                        live_entities.remove(entity)
                        break
                    terrain = gamemap.image.get_at((round(entity.x), round(entity.y)))
                    entity.update(terrain, time.time(), karts = karts, entities = live_entities)
                    if entity.species == 'kart' and not entity.finished:
                        if entity.lap == gamemap.laps:
                            winners.append(entity.image_name)
                            entity.finish(place = len(winners))
                            break
                        get_input(entity, pygame.key.get_pressed())
                cam.update()
            live_entities.update(None, None, -1)
        if gamemode == 3:
            for kart in podium_karts:
                kart.rotation += 0.5
                kart.updated = 0
                kart.update(game.TRACK_BROWN, time.time())
    except AttributeError as e:
        print('! ', e)
    except Exception as e:
        print('an unrecognized error was thrown during game logic')
        exit_game(-1, error = e)

def display(gamemode):
    #render logic
    if gamemode == -1:
        loadscreen()
    if gamemode == 0 or gamemode == 1:
        screen.blit(menu_background, (0, 0))
        current_ui().draw(screen)
    if gamemode == 2:
        screen.fill(game.BLACK)
        for i in range(0, len(cameras)):
            cam = cameras[i]
            active_rect = cam.rect()
            screen_rect = pygame.Rect(cam.width * i, 0, cam.width, cam.height)
            map_image = gamemap.image
            map_sect = map_image.subsurface(active_rect)
            screen.blit(map_sect, ((cam.width + 2) * i, 0))
                
            #displaying on-screen entities
            active_entities = active_rect.collidelistall(
                    [sprite.rect() for sprite in live_entities.sprites()])
            for n in active_entities:
                entity = live_entities.sprites()[n]
                entity_image, entity_rect = entity.animate()
                entity_rect.x -= cam.x - ((WIDTH + 2) * i) 
                entity_rect.y -= cam.y
                if entity_rect.x > screen_rect.x:
                    screen.blit(entity_image, entity_rect)
                    if entity.species == 'kart':
                        if entity.finished:
                            place_text = game.FONT_STANDARD.render(str(entity.finished), True, game.GOLD)
                            text_box = pygame.Surface((place_text.get_width() + 4, place_text.get_height() + 4))
                            text_box.fill(game.BLACK)
                            text_box.blit(place_text, (2, 2))
                            screen.blit(text_box, (entity_rect.x+10, entity_rect.y-32))
            current_kart = karts.sprites()[i]

            #---------UI---------#

            #display powerups
            powerup = pygame.image.load('sprites/powerup_container.png').convert_alpha()
            pu_type = current_kart.powerup
            if pu_type:
                if pu_type == 'shroom':
                    img_name = 'pu_shroom.png'
                elif pu_type == 'banana':
                    img_name = 'trap_banana.png'
                elif pu_type == 'shell_b':
                    img_name = 'trap_shell_b.png'
                elif pu_type == 'shell_f':
                    img_name = 'trap_shell_f.png'
                icon = pygame.image.load('sprites/' + img_name).convert_alpha()
                powerup.blit(icon, (6, 6))
            screen.blit(powerup, ((WIDTH * (i+1)) - powerup.get_width(), 0))

            #signal_img
            rendered_signal_img = pygame.Surface((signal_img.get_width() + 4, signal_img.get_height() + 4))
            rendered_signal_img.fill(game.GOLD)
            rendered_signal_img.blit(signal_img, (2, 2))
            for kart in karts.sprites():
                dot_loc = (round(kart.x/40), round(kart.y/40))
                dot = pygame.Surface((4, 4))
                if kart.image_name == 'mario':
                    dot.fill(game.DOT_M)
                if kart.image_name == 'peach':
                    dot.fill(game.DOT_P)
                if kart.image_name == 'bowser':
                    dot.fill(game.DOT_B)
                if kart.image_name == 'luigi':
                    dot.fill(game.DOT_L)
                rendered_signal_img.blit(dot, dot_loc)
            screen.blit(rendered_signal_img, ((WIDTH * (i+1)) - rendered_signal_img.get_width(), HEIGHT - rendered_signal_img.get_height()))

            #lap and checkpoint
            kart_lap = game.FONT_STANDARD.render('LAPS: ' + str(current_kart.lap), True, game.BLACK)
            kart_stage = game.FONT_STANDARD.render('CHECKPOINT: ' + str(current_kart.stage), True, game.BLACK)
            screen.blit(kart_lap, (((WIDTH + 2) * i) + 5, 5))
            screen.blit(kart_stage, (((WIDTH + 2) * i) + 5, kart_lap.get_height() + 5))
            
            #win msg
            '''if current_kart.finished:
                message = 'You finished'
                if karts.sprites()[i].finished == 1:
                    message += ' first'
                if karts.sprites()[i].finished == 2:
                    message += ' second'
                if karts.sprites()[i].finished == 3:
                    message += ' third'
                message += '!'
                text = game.FONT_BIG.render(message, True, game.WHITE)
                rect = text.get_rect(center = (WIDTH/2 + ((WIDTH + 2) * i), HEIGHT/2))
                wintext = pygame.Surface((rect.width + 10, rect.height + 10))
                wintext.fill(game.BLACK)
                wintext.blit(text, (5, 5))
                screen.blit(wintext, rect)'''
            
            #countdown timing
            if time.time() - mode_time < countdown:
                seconds = math.ceil(countdown - (time.time() - mode_time))
                text = game.FONT_BIG.render(str(seconds), True, game.YELLOW)
                textbox = pygame.Surface((text.get_width() + 10, text.get_height() + 10))
                textbox.blit(text, (5, 5))
                rect = textbox.get_rect(center = (WIDTH/2 + ((WIDTH + 2) * i), HEIGHT/2))
                screen.blit(textbox, rect)
    if gamemode == 3:
        try:
            current_ui().draw(screen)
            for kart in podium_karts.sprites():
                kart_image, kart_rect = kart.animate()
                screen.blit(kart_image, kart_rect)
        except TypeError as e:
            print(e)
    pygame.display.update()

def main():
    global fps
    #displaying a load screen while the menu components are loaded
    loadscreen()
    
    menu_sprites = loadSprites_menu()
    
    start_time = time.time()
    frame_counter = 0
    fps = 0
    while True:
        update(gamemode)
        display(gamemode)
        frame_counter += 1
        if (time.time() - start_time > 1):
            fps = round(frame_counter / (time.time() - start_time))
            frame_counter = 0
            start_time = time.time()
            print(fps)
    
if __name__ == '__main__':
  main()

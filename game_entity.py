import math, time
import pygame
import application_constants as game
import game_images
images = game_images.get_game_images()
s = pygame.sprite

class Entity(s.Sprite):
    def __init__(self, image = game.NOSPRITE, image_name = None, species = 'undefined',#standard shit
                 pos = (0, 0), rotation = 0, speed = 0, ang_speed = 0,#standard shit
                 max_speed = game.BALANCED_MAXSPEED, rate = game.BALANCED_RATE,#don't fuck w/ these 
                 max_rot = game.BALANCED_MAXROT, rate_rot = game.BALANCED_RATEROT,#don't fuck w/ these
                 lifespan = -1,
                 animation = None):#time created, max life in millis; -1 is immortal
        s.Sprite.__init__(self)
        
        if image_name:
            self.image = images[image_name]
            self.image_name = image_name
        else:
            self.image = image
        
        self.species = species
        
        self.x = pos[0]
        self.y = pos[1]
        self.speed = speed
        
        self.rotation = rotation
        self.ang_speed = ang_speed

        self.max_speed = max_speed
        self.max_rot = max_rot
        self.rate = rate
        self.rate_rot = rate_rot

        self.accel = 0
        self.ang_accel = 0

        self.alive = True
        self.lifespan = lifespan
        self.init_time = time.time()
        self.turning = 0

        self.updated = 0
        self.deathcounter = None

        self.animation = animation
        if game.TESTING:
            print('*created Entity of species ', self.species, '\n\tx = ', self.x, '\ty = ', self.y, '\trot = ', self.rotation)
            if image_name:
                print('\timage = ', image_name)
    
    def update(self, terrain, current_time, updated = 1, karts = None, entities = None):
        if updated == -1:
            self.updated = 0
            return
        if self.updated:
            return
        if self.lifespan > 0:
            if time.time() - self.init_time >= self.lifespan:
                self.die()
        self.updated = 1
        rate = self.rate
        rate_rot = self.rate_rot
        max_rot = self.max_rot
        #terrain-specific logic
        if terrain == game.TRACK_BROWN or terrain == game.TRACK_GRAY:
            max_speed = self.max_speed
            resistance = game.BALANCED_RESISTANCE
        else:
            max_speed = game.BALANACED_MAXSPEED_SLOW
            rate = game.BALANCED_RATE_SLOW
            resistance = game.BALANCED_RESISTANCE_SLOW
        if terrain == game.WATER or terrain == game.LAVA:
            self.die()

        #accel/decel
        if self.accel:
            if self.speed < max_speed:
                self.speed += rate
            else:
                self.speed -= rate
        elif self.speed > 0:
            self.speed -= resistance
            if self.speed < 0:
                self.speed = 0

        #angular accel/decel
        if self.turning == 1:
            if self.ang_speed < max_rot:
                self.ang_speed += rate_rot
        elif self.turning == -1:
            if self.ang_speed > -max_rot:
                self.ang_speed -= rate_rot
        else:
            if self.ang_speed > 0:
                self.ang_speed -= rate_rot * 4
                if self.ang_speed < 0:
                    self.ang_speed = 0
            if self.ang_speed < 0:
                self.ang_speed += rate_rot * 4
                if self.ang_speed > 0:
                    self.ang_speed = 0

        self.x += -self.speed * math.cos(math.radians(self.rotation+90)) * game.MOVE_SCALER
        self.y += -self.speed * math.sin(math.radians(self.rotation+90)) * game.MOVE_SCALER
        self.rotation += self.ang_speed * game.MOVE_SCALER
        if self.rotation > 360:
            self.rotation -= 360
        if self.rotation < 0:
            self.rotation += 360
    
    def die(self):
        #placeholder, override with situational on-death logic
        self.alive = False
    
    def animate(self):
        if not self.animation:
            rect = self.image.get_rect(center = (self.x, self.y))
            return self.image, rect
        elif self.animation == 'r':
            rot_img = pygame.transform.rotate(self.image, self.rotation-90)
            rect = rot_img.get_rect(center = (self.x, self.y))
            return rot_img, rect
        elif self.animation[2] == 'r-s':#symmetric rotation
            animation_width = self.animation[0][0]
            animation_height = self.animation[0][1]
            animation_stage = round(((self.rotation) / self.animation[1]) - 0.5)
            index = -abs(animation_stage - 12) + 12
            if index < 11 and index > 4:
                index += 1
            if index > 7:
                index -= 1
            sub_rect = pygame.Rect(animation_width * index, 0, animation_width, animation_height)
            current_frame = self.image.subsurface(sub_rect)
            if animation_stage > 11:
                current_frame = pygame.transform.flip(current_frame, True, False)
            current_rect = current_frame.get_rect(center = (self.x, self.y))
            return current_frame, current_rect
    
    def rect(self):
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
    
class Kart(Entity):
    def __init__(self, key_accel, key_right, key_left, key_use,
                 image = None, image_name = None, species = 'kart',
                 pos = (0, 0), rotation = 0, speed = 0, ang_speed = 0,
                 max_speed = game.BALANCED_MAXSPEED, rate = game.BALANCED_RATE,
                 max_rot = game.BALANCED_MAXROT, rate_rot = game.BALANCED_RATEROT,
                 lifespan = -1,
                 animation = None):
        Entity.__init__(self, image, image_name, species, pos, rotation, speed, ang_speed,
                        max_speed, rate, max_rot, rate_rot,
                        lifespan, animation)
        self.ACCEL = key_accel
        self.TURN_RIGHT = key_right
        self.TURN_LEFT = key_left
        self.USE = key_use
        self.powerup = None
        self.use = False
        self.lap = 0
        self.stage = 0
        self.finished = 0
        self.respawn = self.x, self.y, self.rotation
        if not key_accel:
            key_accel, key_right, key_left, key_use = game.KEYSET_DEFAULT

    def set_accel(self, value):
        self.accel = value

    def set_turn(self, value):
        self.turning = value

    def use_item(self):
        self.use = True
    
    def die(self):
        self.deathcounter = time.time()

    def spawn(self):
        self.speed = 0
        self.ang_speed = 0
        self.x, self.y, self.rotation = self.respawn
        self.deathcounter = None

    def effect(self, value):
        if value == 'boost':
            self.speed += self.max_speed
        elif value == 'stun':
            self.ang_speed = 7
        elif value == 'kill':
            self.die()

    def finish(self, place):
        self.accel = False
        self.turning = True
        self.finished = place

    def update(self, terrain, current_time, updated = 1, karts = None, entities = None):
        if self.deathcounter:
            if time.time() - self.deathcounter > 1:
                self.spawn()
            return
        Entity.update(self, terrain, current_time, updated, karts)
        if self.stage > 4:
            self.stage = 0
            self.lap += 1
        if self.use:
            if self.powerup == 'shroom':
                self.effect('boost')
            elif self.powerup == 'banana':
                trap = Trap('stun', image_name = 'trap_banana',
                            pos = (round(self.x) + (40 * math.cos(math.radians(self.rotation+90))), round(self.y) + (40 * math.sin(math.radians(self.rotation+90)))),
                            rotation = self.rotation-180, speed = 0.5)
                entities.add(trap)
            elif self.powerup == 'shell_f':
                trap = Trap('kill', image_name = 'trap_shell_f',
                            pos = (round(self.x) - (40 * math.cos(math.radians(self.rotation+90))), round(self.y) - (40 * math.sin(math.radians(self.rotation+90)))),
                            rotation = self.rotation, speed = 8,
                            lifespan = 10)
                entities.add(trap)
            elif self.powerup == 'shell_b':
                trap = Trap('kill', image_name = 'trap_shell_b',
                            pos = (round(self.x) + (40 * math.cos(math.radians(self.rotation+90))), round(self.y) + (40 * math.sin(math.radians(self.rotation+90)))),
                            rotation = self.rotation-180, speed = 4,
                            lifespan = 10)
                entities.add(trap)
            self.use = False
            self.powerup = None

class Powerup(Entity):
    def __init__(self, pu_type,
                 image = None, image_name = 'powerup_box', species = 'powerup',
                 pos = (0, 0), rotation = 0, speed = 0, ang_speed = 0,
                 max_speed = game.BALANCED_MAXSPEED, rate = game.BALANCED_RATE,
                 max_rot = game.BALANCED_MAXROT, rate_rot = game.BALANCED_RATEROT,
                 lifespan = 45,
                 animation = None):
        Entity.__init__(self, image, image_name, species, pos, rotation, speed, ang_speed,
                        max_speed, rate, max_rot, rate_rot,
                        lifespan, animation)
        self.pu_type = pu_type
        
    def update(self, terrain, current_time, updated = 1, karts = None, entities = None):
        Entity.update(self, terrain, current_time, updated, karts, entities)
        rect = self.image.get_rect(center = (self.x, self.y))
        if not karts: return
        for kart in karts:
            kart_rect = kart.animate()[1]
            if rect.colliderect(kart_rect):
                if not kart.powerup: kart.powerup = self.pu_type
                self.die()

class Trap(Entity):
    def __init__(self, trap_type,
                 image = None, image_name = None, species = 'trap',
                 pos = (0, 0), rotation = 0, speed = 0, ang_speed = 0,
                 max_speed = game.BALANCED_MAXSPEED + 1, rate = game.BALANCED_RATE,
                 max_rot = game.BALANCED_MAXROT, rate_rot = game.BALANCED_RATEROT,
                 lifespan = -1,
                 animation = None):
        Entity.__init__(self, image, image_name, species, pos, rotation, speed, ang_speed,
                        max_speed, rate, max_rot, rate_rot,
                        lifespan, animation)
        self.trap_type = trap_type
        
    def update(self, terrain, current_time, updated = 1, karts = None, entities = None):
        Entity.update(self, terrain, current_time, updated, karts, entities)
        rect = self.animate()[1] 
        if not karts: return
        for kart in karts:
            kart_rect = kart.animate()[1]
            if rect.colliderect(kart_rect):
                kart.effect(self.trap_type)
                self.die()

class Checkpoint(Entity):
    def __init__(self, stage = -1,
                 image = None, image_name = None, species = 'checkpoint',
                 pos = (0, 0), rotation = 0, speed = 0, ang_speed = 0,
                 max_speed = game.BALANCED_MAXSPEED, rate = game.BALANCED_RATE,
                 max_rot = game.BALANCED_MAXROT, rate_rot = game.BALANCED_RATEROT,
                 lifespan = -1,
                 animation = None):
        Entity.__init__(self, image, image_name, species, pos, rotation, speed, ang_speed,
                        max_speed, rate, max_rot, rate_rot,
                        lifespan, animation)
        self.stage = stage
    
    def update(self, terrain, current_time, updated = 1, karts = None, entities = None):
        Entity.update(self, terrain, current_time, updated, karts, entities)
        if not karts: return
        rect = self.animate()[1]      
        for kart in karts:
            kart_rect = kart.animate()[1]
            if rect.colliderect(kart_rect):
                if kart.stage == self.stage:
                    kart.stage += 1
                    kart.respawn = (self.x, self.y, self.rotation)


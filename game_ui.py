import pygame
import application_constants as game
import game_images
ui_images = game_images.get_ui_images()

def button_default():
    print('this button is useless!')

class Element(pygame.sprite.Sprite):
    def __init__(self, text = None, pos = (0, 0),
                 image = None, image_name = None, offset = None, text_color = None, centered = False):
        pygame.sprite.Sprite.__init__(self)
        
        if text:
            text_surface = game.FONT_STANDARD.render(text, False, game.WHITE)
        else:
            text_surface = pygame.Surface((0, 0))
        
        if image:
            self.image = image
        elif image_name:
            self.image = ui_images[image_name]
        else: 
            self.image = pygame.Surface((
                (text_surface.get_width()+40),
                (text_surface.get_height()+10)))
            
        if not offset:
            offset = (
                (self.image.get_width()-text_surface.get_width())/2,
                (self.image.get_height()-text_surface.get_height())/2)
        self.image.blit(text_surface, offset)
        
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        if centered:
            self.rect.x += (game.WIDTH-self.image.get_width())/2
            self.rect.y += (game.HEIGHT-self.image.get_height())/2

    def set_image(self, image = None, image_name = None):
        if image:
            self.image = image
        elif image_name:
            self.image = ui_images[image_name]
        else:
            return

class Popup(Element):
    def __init__(self, text = '!',
                 pos = (0, 0), image = None, image_name = None, offset = None, text_color = game.YELLOW):
        Element.__init__(self, text, pos, image, image_name, offset, text_color, centered = True)
    
class Button(Element):
    def __init__(self, text = None,
                 pos = (0, 0), image = None, image_name = None, offset = None, text_color = None, centered = False,
                 onclick = button_default, arg = None):
        Element.__init__(self, text, pos, image, image_name, offset, text_color, centered)
        self.onclick = onclick
        self.arg = arg
        
    def clicked(self):
        if self.arg:
            self.onclick(self.arg)
        else:
            self.onclick()

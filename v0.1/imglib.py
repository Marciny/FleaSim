import pygame, os
from pygame.locals import *

class SpriteSheet:
    def __init__(self, filename):
        self.sheet = load_image(filename)
    def imgat(self, rect, colorkey = None):
        rect = Rect(rect)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        return imgcolorkey(image, colorkey)
    def imgsat(self, rects, colorkey = None):
        imgs = []
        for rect in rects:
            imgs.append(self.imgat(rect, colorkey))
        return imgs

def load_image(filename, colorkey = None):
    filename = os.path.join('data', filename)
    image = pygame.image.load(filename).convert()
    return imgcolorkey(image, colorkey)

def imgcolorkey(image, colorkey):
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image

def text_objects(text, color, font):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def msg2screen (msg, color, font, screen, pos, rectref='topright'):
    textSurf, textRect = text_objects(msg, color, font)
    setattr(textRect, rectref, pos)
    screen.blit(textSurf, textRect)

class Potbar(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.base_image = image
        self.base_image.set_colorkey((255,0,255))
        self.image = self.base_image
        self.length = 96
        self.rect= self.image.get_rect()
    def update(self, potency_ratio):
        self.fill_length = round(potency_ratio*self.length)
        self.image.fill( (235,235,235), (2,2,96,16) )
        self.image.fill( (255,0,255), (2,2,96 - self.fill_length,16) )

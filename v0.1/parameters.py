import pygame, os, numpy
from imglib import *
# settings, poziom trudności
fps = 30

max_bites = 2 # ile mozna "wygryzc" ze skory
bitealpha = round(255/max_bites)
max_bitelist = 4
bitelist_threshhold = 3500 * max_bites# *100 ###
slap_threshold  = 35000 * max_bites #*100 ###
potency_threshold = 2500
max_potency = 5 * potency_threshold
secondary_potency = round (potency_threshold / 4)
no_AIs = 1
powerup_spawn_time = 4 * fps
powerup_life_time = 6 * fps # *100
powerup_effect_time =  6 * fps # * 100
scratch_freq = 4 * fps




#background , mapa, pochodne
bgname = 'sk1600.jpg' 
background = pygame.image.load(os.path.join('data', bgname)) #sk1600.jpg
_,_, map_width, map_height = background.get_rect()
map_area = map_width * map_height
max_bitten_area = 2 * map_area # maxymalna powierzchnia maxymalnego ugryzienia
screen_width = min(1000, map_width)
half_width = int(screen_width/2)
screen_height = min(700, map_height)
half_height = int(screen_height/2)
size = screen_width, screen_height


#display
pygame.init()
icon = pygame.image.load((os.path.join('data', 'icon.gif')))
##icon = pygame.image.load((os.path.join('data', 'flea_side.gif')))
##icon.set_colorkey((255,255,255))
pygame.display.set_icon(icon)
pygame.display.set_caption('Fleating Experience')
screen = pygame.display.set_mode(size)

# inicializacja uobrazkow
background.convert()
font = pygame.font.SysFont('arialpogrubiony', 20)
biggerfont = pygame.font.SysFont('calibri', 35)
gover_font = pygame.font.SysFont('bankgothicmedium', 100)
spritesheet = SpriteSheet('tiles.bmp')
powerup_sheet = SpriteSheet('powerups.png')

#soundy
pre_jump = pygame.mixer.Sound(os.path.join('data', 'balloon.wav'))
jump_sound = pygame.mixer.Sound(os.path.join('data', 'spin_jump.wav'))
bite_sound = pygame.mixer.Sound(os.path.join('data', 'bite.wav'))

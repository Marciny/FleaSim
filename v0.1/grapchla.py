import pygame, random, os, time, pygame.gfxdraw, numpy#, globs #, cam
##from flea import *
from pygame.locals import *
from matlib import *
from parameters import *
from cam import *
from other_funcs import *


##display_loop  = 0
###


class Flea(pygame.sprite.Sprite):
    
    def __init__(self, pos, control, sex, ID, containers, image=None ):
        self.containers = containers
##        pygame.sprite.Sprite.__init__(self, self.containers)
        super().__init__(self.containers)
        self.ID = ID
        self.pos = pos
        self.control = control
        self.sex = sex
        if not image:
            if sex == 'male':
                self.base_image = self.image_m
            else:
                self.base_image = self.image_f
        else:
            self.base_image= image

        self.augmented_image = self.base_image
        self.image = self.augmented_image
        self.rect = self.image.get_rect()
        self.rect.center= self.pos
        
        self.size = 10
        self.power = 5
        self.powerups = []
        self.delayed = []
        self.power_mod = 1
        self.jump_mod = 1
        self.angle = 0
        self.score_temp = 0
        self.score = 0
        self.potency = 0
        self.children = 0
        self.freeze = 0
        self.counter = 0
        self.dead = False
        self.motion_speed = 0.1
        self.motion_frames = round(self.motion_speed * fps)

    def ini_jump(self, angle, jumplength):
        """ ini_jump jest od kontrolowania, czy pchua jest w trakcie skoku; jeśli tak, to wykonuje kolejny skoczek i zamraża pchłę na inne akcje,
            jeśli nie, to resetuje zamrożenie i licznik.
            ini_jump jest wywoływane wielokrotnie i robi mały skoczek (z większego, przedzielonego przez liczbę klatek)""" 
        if self.counter < self.motion_frames:
            self.freeze = 1
            jumplength = jumplength/self.motion_frames * self.jump_mod 
            self.jump(angle, jumplength)
            self.counter += 1
        elif not self.dead:
            self.freeze = 0
            self.counter = 0
        
        
    def jump(self, angle, jumplength):
        case = [0,0]
        addvector = angle_dist_to_vector(angle, jumplength)
        finpos = (self.pos[0] + addvector[0], self.pos[1] - addvector[1]) # - addvector[1], bo czecia ćwiartka - ot specyfika funkcji
        if finpos[0] < 0  or finpos[0] > map_width or finpos[1] < 0 or finpos[1] > map_height :   # spr, czy skok wychodzi poza mapkę, a może rect.contains?
            reversedvector = tuple(reversed(addvector))
            dist_to_left = 123456789
            dist_to_right = 123456789
            dist_to_top = 123456789
            dist_to_bottom = 123456789
            if finpos[0] < 0 :
                dist_to_left = vector_to_dist((self.pos[0],
                                              vecterp(addvector ,self.pos[0])))
            elif finpos[0] > map_width:
                dist_to_right = vector_to_dist((map_width-self.pos[0],
                                              vecterp(addvector , map_width-self.pos[0])))
            if finpos[1] < 0 :
                dist_to_top = vector_to_dist((self.pos[1],
                                              vecterp(reversedvector ,self.pos[1])))
            elif finpos[1] > map_height:
                dist_to_bottom = vector_to_dist((map_height-self.pos[1],
                                              vecterp(reversedvector , map_height-self.pos[1])))
            if dist_to_left == min(dist_to_left, dist_to_right, dist_to_top, dist_to_bottom):
                self.onejump( angle, dist_to_left)
                self.angle = angle_mirror_y (angle)
                self.jump( self.angle, jumplength - dist_to_left)
            elif dist_to_right == min(dist_to_left, dist_to_right, dist_to_top, dist_to_bottom):
                self.onejump( angle, dist_to_right)
                self.angle = angle_mirror_y (angle)
                self.jump( self.angle, jumplength - dist_to_right)
            elif dist_to_top == min(dist_to_left, dist_to_right, dist_to_top, dist_to_bottom):
                self.onejump( angle, dist_to_top)
                self.angle = angle_mirror_x (angle)
                self.jump( self.angle, jumplength - dist_to_top)
            else:
                self.onejump( angle, dist_to_bottom)
                self.angle = angle_mirror_x (angle)
                self.jump( self.angle, jumplength - dist_to_bottom)
                
        else :
            self.onejump(angle, jumplength)
            
    def onejump (self, angle, jumplength):
        addvector = angle_dist_to_vector(angle, jumplength)
        # "animacja"
        self.image = pygame.transform.rotate(self.augmented_image, angle)
        self.rect = self.image.get_rect()
        self.rect.center = camera.posupd(self.pos)
##        if LAST_FPS > 25:
##            screen.blit(self.image, ( self.rect.topleft[0] + addvector[0]/2 , 
##                                 self.rect.topleft[1] - addvector[1]/2 ))
        # rysowanie pchły pomiędzy położeniem początkowym i końcowym - daje większe złudzenie płynności, a nie wpływa znacząco negatywnie na szybkość
        screen.blit(self.image, ( self.rect.topleft[0] + addvector[0]/2 , 
                                 self.rect.topleft[1] - addvector[1]/2 ))
        
        self.pos = (self.pos[0] + addvector[0], self.pos[1] - addvector[1]) # - add..[1], bo jestesmy w 3 cwiartce


    def dorandom(self):
        if self.control == "AI":
            if not self.freeze:
                randnumber = random.randrange(0, fps * 2 ,1)
                if randnumber >= 11 and randnumber <= 14: 
                    self.angle += random.randrange(-90, 91 ,1)
                    if self.angle < 0 :
                        self.angle += 360
                if randnumber == 23:
                    self.jlength = random.randrange(0,400,1)
                    self.ini_jump(self.angle, self.jlength)
                    
                elif randnumber == 37 or randnumber == 8:
                    self.bite()
            elif not self.dead:
                self.ini_jump(self.angle, self.jlength)

    def bite (self):
        if not self.freeze:
            global map_array, background, globscore, map_array, ID, map_width, map_height, all_, AIs, bitten_area
            # ugryzienie per se
            rbpos = (round(self.pos[0]), round(self.pos[1]))
##            mappos= (rbpos[0] +200, rbpos[1] + 200)
            self.final_power = round(self.power * self.power_mod)
            pygame.gfxdraw.filled_circle(background, rbpos[0], rbpos[1], self.final_power, (255,0,0,bitealpha)) #bylo alpha 85
            mx1, mx2 = max(0, rbpos[0]-self.final_power), min(map_width -1, rbpos[0]+self.final_power)
            my1, my2 = max(0, rbpos[1]-self.final_power), min(map_height -1, rbpos[1]+self.final_power)
            for row in range(mx1, mx2):
                for col in range (my1, my2):
                    if map_array[row,col] < max_bites:  # 
                        map_array[row,col] += 1
                        self.score_temp += 1
                        
            # przyrost punktów, mocy
            self.score +=  self.score_temp
            bitten_area += self.score_temp
            globscore +=  self.score_temp
            if self.potency < max_potency:
                self.potency += self.score_temp
                self.potency = min(max_potency, self.potency)
            
            self.size = 10 + round(math.sqrt(self.score/250))
            self.augmented_image = pygame.transform.scale(self.base_image,
                                                            (self.size, self.size)) # przyrost mięcha po jedzonku
            self.power = round(5+ math.sqrt(self.score/800)) # przyrost mocy po jedzonku
            self.score_temp = 0
            
            # wywoływanie slapów:
            if len(bitelist) <= max_bitelist:
                bmx1, bmx2 = max(0, rbpos[0]-100), min(map_width -1, rbpos[0]+100)
                bmy1, bmy2 = max(0, rbpos[1]-100), min(map_height -1, rbpos[1]+100)
                mpsum = map_array[bmx1 : bmx2, bmy1 : bmy2].sum()
                if mpsum >= bitelist_threshhold:
                    bitelist.append((rbpos, mpsum))

            # prokreacja :
            if self.potency >= potency_threshold:  
                for i in fleas :
                    if  self.rect.collidepoint(i.rect.center) \
                       and self.sex != i.sex \
                       and i.potency >= secondary_potency:
                        for j in range(0,(random.randrange(1,5))):
                            
                            Flea( (random.randrange(10, map_width - 10,1), random.randrange(10, map_height - 10,1)), 'AI',
                                  random.choice(('male', 'female')), ID, (all_, AIs, fleas))
                            ID += 1
                            self.children += 1
                        self.potency -= potency_threshold
                        i.potency -= secondary_potency
                        globscore += 5000 + self.children * 300


    def update(self):
        global max_potency
##        if self.control == "player" :   # kąt z powodu pozycji myszy apdejtowany tylko dla gracza; tak samo offset kamery apdejtowany tylko raz(mógłym to wywalić gdzieś poza klasę)
##            if not self.freeze:
##                self.angle =  vector_to_angle(mousepos, self.rect.center)[1]
        self.image = pygame.transform.rotate(self.augmented_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = camera.posupd(self.pos)
        #
        self.jump_count = 0
        self.power_count = 0
        for i in range(len(self.powerups)-1, -1,  -1 ):
            self.powerups[i][1] -= 1
            if self.powerups[i][1] == 0:
                del(self.powerups[i])
        for x in self.powerups:
            if x[0] == 'speed':
               self.jump_count += 1
            elif x[0] == 'power' :
                self.power_count += 1
        self.jump_mod = round( math.pow(2, self.jump_count))
        self.power_mod =  math.pow(1.5, self.power_count)
        
        if self.delayed:
            self.update_delayed()


    def delay(self, counter, func, *args):
        self.delayed.append([ counter, func, args])

    def update_delayed(self):
       for i in range(len(self.delayed)-1, -1,  -1 ):
            if self.delayed[i][0] == 0 :
                args = self.delayed[i][2]
                self.delayed[i][1](*args)
                del(self.delayed[i])
            else:
                self.delayed[i][0] -= 1


    def die(self):
        if not self.dead:
            global ID, deadgroup, GAMEOVER, AIs, player
            self.dead = True
            self.kill()
##            for i in self.containers:
##                i.remove(self)
            pygame.sprite.Sprite.__init__(self, deadgroup)
            self.powerups = []
            self.freeze = 1
            self.img_nr = random.randrange(0,2)
            if self.base_image == self.image_m:
                if self.img_nr == 0:
                    self.base_image = self.image_m_dead
                else:
                    self.base_image = self.image_m_dead2
            else:
                if self.img_nr == 0:
                    self.base_image = self.image_f_dead
                else:
                    self.base_image = self.image_f_dead2
                
            self.augmented_image = pygame.transform.scale(self.base_image, (self.size, self.size)) # UWAGA: sprajt się trochę zmniejsza, z tego powodu, że zwykły rozmiar = 10, a zdechnięty = 12
            self.image = pygame.transform.rotate(self.augmented_image, self.angle)
            ID -= 1
            if ID == -1:
                GAMEOVER = True
            self.ID = 54321
            self.rect.center = self.pos
            deadmap.blit(self.image, ( self.rect.topleft[0], 
                                 self.rect.topleft[1] ))
            # rezurekcija
            if self.control == 'player':
                if AIs.sprites():
                    x = random.randrange(0,len(AIs.sprites()))
                    player = AIs.sprites()[x]
                    player.remove(AIs)
                    print(player.containers)
                    print(self.containers)
                    
                    player.control = 'player'
                    player.delay( 1.5 * fps, camera.center, player.pos)
##                                        player.delayed.append( [1 * fps, camera.center, player.pos])



class Slap(pygame.sprite.Sprite):
    def __init__(self, pos, slapmod=0):
        super().__init__(self.containers)
        self.size = 200 + slapmod
        self.speed = 2
        self.frspeed = self.speed * fps
        self.counter = 0
        self.pos = [pos[0] + random.randrange(-50,50,1),pos[1] + random.randrange(-50,50,1) ]
        self.rect = pygame.Rect((0,0), (self.size, self.size))
        self.rect.center = camera.posupd(self.pos)
    def update(self):
        if self.counter < self.frspeed:
            self.alpha = math.ceil(200/self.frspeed*self.counter)
            self.printpos = camera.posupd(self.pos)
            self.printdiameter = round(self.size/2) #+  self.frspeed - self.counter)
            pygame.gfxdraw.filled_circle(screen, self.printpos[0], self.printpos[1], self.printdiameter,
                                         (0,0,0, self.alpha))
            self.counter += 1
        elif self.counter == self.frspeed:
            self.rect.center = camera.posupd(self.pos)
            for i in all_ :
                if self.rect.colliderect(i.rect) \
                   and vector_to_dist((self.rect.center[0] - i.rect.center[0],
                                      self.rect.center[1] - i.rect.center[1])) \
                                      <= self.size/2:
                    i.die()
                
            self.kill()
            

class ScratchGen(pygame.sprite.RenderUpdates):
    def __init__(self):
        super().__init__()
        self.gen_list = []
        self.speed = 1
##        self.threshold = threshold
    def update(self, globscore):
        super().update()
        if globscore >= scratch_threshold:
            if not self.gen_list:
                self.gen_list = [[scratch_freq , scratch_freq ]]
                print(self.gen_list)
            if globscore >= 2 * scratch_threshold:
                self.gen_list = [[scratch_freq , scratch_freq ], [scratch_freq , scratch_freq ]]
            for x in self.gen_list:
                if x[1] == 0:
                    Scratch(self, self.speed)
                    x[1] = x[0]
                    self.speed += 0.05
                else:
                    x[1] -= 1


class Scratch(pygame.sprite.Sprite):
    def __init__(self, containers, speed):
        self.containers = containers
        super().__init__(self.containers)
        self.speed = speed
        self.start = random.choice(('top', 'bottom', 'right', 'left'))
        if self.start == 'top':
            self.pos = [random.randrange(0, map_width - 15), 0]
            self.dir = 'bottom'
            self.angle = 180 + random.randrange(-30,31)
        elif self.start == 'bottom':
            self.pos = [random.randrange(0, map_width - 15), map_height]
            self.dir = 'top'
            self.angle = minus_angle_convert( 0 + random.randrange(-30,31))
        elif self.start == 'left':
            self.pos = [0, random.randrange(0, map_height - 15)]
            self.dir = 'right'
            self.angle = 270 + random.randrange(-30,31)
        elif self.start == 'right':
            self.pos = [map_width, random.randrange(0, map_height - 15)]
            self.dir = 'left'
            self.angle = 90 + random.randrange(-30,31)
        self.movement = angle_dist_to_vector(self.angle, 1)
##        self.rect = self.image.get_rect()
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center= camera.posupd(self.pos)
    def update(self):
        global globscore
##        self.rect.move(self.movement[0], self.movement[1])
        self.pos = [self.pos[0]+ round(self.movement[0]*10* self.speed),
                    self.pos[1] - round (self.movement[1]*10* self.speed)]
        self.rect.center= camera.posupd(self.pos)
        for i in fleas:
            if self.rect.collidepoint(i.rect.center):
                i.die()
        if self.pos[0] < -200 or self.pos[0] > map_width + 200 \
           or self.pos[1] < -200 or self.pos[1] > map_height +200:
            self.kill()
            if not GAMEOVER:
                globscore += 1000
##        print(self.pos)
       

class Powerup(pygame.sprite.Sprite):
    def __init__ (self, spawnpoint):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.pos = spawnpoint
        self.type = random.choice(('speed', 'power', 'spawn'))
        if self.type == 'speed':
            self.image = self.image_speed
        elif self.type == 'power':
            self.image = self.image_power
        else:
            self.image = self.image_spawn
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.counter = powerup_life_time

    def update(self):
        global ID
        self.rect.center = camera.posupd(self.pos)
        self.counter -= 1
        if self.counter == 0:
            self.kill()
        if pygame.sprite.spritecollideany(self, fleas):
            i = pygame.sprite.spritecollideany(self, fleas)
            if not i.freeze:
                if self.type == 'spawn':
                    ID += 1
                    Flea( (random.randrange(10, map_width - 10,1),
                           random.randrange(10, map_height - 10,1)),
                          'AI', random.choice(('male', 'female')), ID, (all_, AIs, fleas))
                else:
                    i.powerups.append([self.type, powerup_effect_time])
                    print(i.powerups)
                self.kill()
        
        
        
def biteslap():
    global  slapmod
    slapargs = random.choice(bitelist)
    bitelist.remove(slapargs)
    if slapargs[1] > random.randrange(0, slap_threshold) and random.randrange(0,2) == 1:
        slapmod += 1
        return slapargs


def initial_state():
    global GAMEOVER, globscore, ID, bitelist, frame, time, clicked, counter, \
    LAST_FPS, MAX_POP, slapmod, fleaseconds, bitten_area, \
    all_, fleas, AIs, deadgroup, slaps, powerups, deadmap, background, player
    
    GAMEOVER = False
    globscore = 0
    ID = 0
    bitelist = []
    frame = 0
    time = 0
    clicked = 0
    counter = 0
    LAST_FPS = 30
    MAX_POP = 0
    slapmod = 0
    fleaseconds = 0
    bitten_area = 0
    
    all_.remove()
    fleas.remove()
    AIs.remove()
    deadgroup.remove()
    slaps.remove()
    powerups.remove()
    deadmap.fill((255,255,255))
    background = pygame.image.load(os.path.join('data', bgname))

    #player, AI
    player = Flea((random.randrange(10, map_width - 10,1),
                random.randrange(10, map_height - 10,1)), 'player', 'male', 0, (all_, fleas))
       
    for i in range(0,no_AIs):
        ID += 1
        if i == 0 :
            Flea( (random.randrange(10, map_width - 10,1),
                random.randrange(10, map_height - 10,1)),
                    'AI', opposite_sex(player.sex), ID, (all_, AIs, fleas))
        else:
            Flea( (random.randrange(10, map_width - 10,1),
                random.randrange(10, map_height - 10,1)),
                    'AI', random.choice(('male', 'female')), ID, (all_, AIs, fleas))
            
    camera.center(player.pos)

def toggle(dispmod):
    if dispmod == 0 :
        return 1
    elif dispmod == 1:
        return 2
    else:
        return 0

##################################################################################################################   
#initial variables



# wartości zależne od rozmiaru mapy
map_array = numpy.zeros((map_width, map_height))
deadmap = pygame.Surface((map_width, map_height))
deadmap.set_colorkey((255,255,255))
randbite_start = map_width * map_height / 2
scratch_threshold =   map_width * map_height / 12 * max_bites #* 100 # 10000000000

# przypisanie obrazkow

Flea.image_m=spritesheet.imgat((0, 32, 10, 10), -1)
Flea.image_f=spritesheet.imgat((0, 42, 10, 10), -1)
Flea.image_m_dead=spritesheet.imgat((0, 52, 12, 12), -1)
Flea.image_f_dead=spritesheet.imgat((0, 64, 12, 12), -1)
Flea.image_m_dead2=spritesheet.imgat((0, 76, 12, 12), -1)
Flea.image_f_dead2=spritesheet.imgat((0, 88, 12, 12), -1)

Scratch.image = pygame.image.load((os.path.join('data', 'scratch.png')))
Scratch.image.set_colorkey((255,0,255))
Scratch.image = pygame.transform.rotate(Scratch.image, -90)

Powerup.image_speed = powerup_sheet.imgat((0,0,20,20), -1)
Powerup.image_power = powerup_sheet.imgat((20,0,20,20), -1)
Powerup.image_spawn = powerup_sheet.imgat((40,0,20,20), -1)

gui_p_speed =  powerup_sheet.imgat((0,20,20,20), -1)
gui_p_power = powerup_sheet.imgat((20,20,20,20), -1)

jumpbar = spritesheet.imgat((0, 0, 48, 18), (255,255,255))
jumpbarprint=pygame.Surface((48,18))
jumpbarprint.set_colorkey((255,255,255))
jumpbarframe = spritesheet.imgat((98, 0, 54, 20), (255,255,255))
jbarcords = (10,5)
potcords = (150,5)

potbar_img = pygame.image.load((os.path.join('data', 'potbar.png')))
potbar = Potbar(potbar_img)

#grupy
all_ = pygame.sprite.RenderUpdates()
fleas = pygame.sprite.Group()
AIs = pygame.sprite.Group()
deadgroup = pygame.sprite.Group()
slaps = pygame.sprite.RenderUpdates()
Slap.containers = slaps
powerups = pygame.sprite.Group()
Powerup.containers = powerups
scratchgen = ScratchGen()
clock = pygame.time.Clock()
dispmod = 1 # default text display mode

initial_state()


##############################################################################################
# game loop
running = True
while running:

    for event in pygame.event.get():
        if event.type == QUIT   \
           or (event.type == KEYDOWN and    \
               event.key == K_ESCAPE):
##            return
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2] \
             and not player.freeze and not player.dead: # prawyklik
            bite_sound.play()
            player.bite()

        elif event.type == KEYDOWN and event.key == K_SPACE: # centrowanie na graczu za pomocą spacji
            camera.center(player.pos)
        
        elif event.type == KEYDOWN and event.key == K_TAB:
            dispmod = toggle(dispmod)
#####
    mousepos=pygame.mouse.get_pos()
    player.angle =  vector_to_angle(mousepos, player.rect.center)[1]
    camera.update(mousepos)

    if len(powerups) < 3 :
        if random.randrange(0, powerup_spawn_time) == 13:
            Powerup((random.randrange(10, map_width - 20,1),
            random.randrange(10, map_height - 20,1)))    

    
    all_.update()
    powerups.update()
    scratchgen.update(globscore)
##        all_.clear(screen, background)

    screen.blit(background, camera.offset)
    screen.blit(deadmap, camera.offset)
    powerups.draw(screen)   
    all_.draw(screen)
    scratchgen.draw(screen)
    
    
    for i in AIs:
        i.dorandom()
        
##    screen.blit( statusbar, (0, barpos, screen_width, bar_height ) )
    potbar.update(player.potency/max_potency)
    if dispmod > 0 :
        screen.blit(jumpbarframe, jbarcords)
        screen.blit(potbar.image, potcords)
        powerups_pos = [350, 5]
        for x in player.powerups:
            if x[0] == 'speed':
                screen.blit(gui_p_speed, (powerups_pos))
            elif x[0] == 'power':
                screen.blit(gui_p_power, (powerups_pos))
            powerups_pos[0] += 25
##    screen.fill((32,32,32,100), (0, barpos, screen_width, bar_height ))

            # lklik
    if not player.freeze :
        if pygame.mouse.get_pressed()[0] == 1:
            if clicked == 0:
                pre_jump.play()
                clicked = 1
            counter = counter +1
            j_width, j_height=jumpbar.get_rect().size
            for i in range(0,j_width):
                for j in range(0,j_height):
                    if counter/fps/5*j_width > j_width - i:
                        jumpbarprint.set_at((i,j), jumpbar.get_at((i,j)))
                    else:
                        jumpbarprint.set_at((i,j), (255,255,255))
            if dispmod > 0:
                screen.blit(jumpbarprint, jbarcords)
          
        elif pygame.mouse.get_pressed()[0] == 0 and counter > 0:
            pre_jump.stop() 
            jump_sound.play()
            player.ini_jump(player.angle, jump_length(counter, fps))

            
    else: 
        player.ini_jump(player.angle, jump_length(counter, fps))
        if player.counter == player.motion_frames:
            clicked = 0
            counter = 0

# dodatkowe difikulti
    if globscore > randbite_start and len(bitelist) <= max_bitelist \
       and random.randrange(0, round(1 * fps), 1) == 6 :
        print('jest')
        bitelist.append((randpoint((0,map_width), (0, map_height), 1),
                         random.randrange(0, 2 * slap_threshold, 1) + (globscore/randbite_start - 1) * 5000 ))
    
    if bitelist :
        b = biteslap()
        if b:
            Slap(b[0], slapmod)

    
    slaps.update()
# napisy
    POP = ID +1
    MAX_POP = max(POP, MAX_POP)
    bitten_area_percent = round(bitten_area / max_bitten_area * 100, 1)
    frame += 1
    if frame == fps:
        frame = 0
        time += 1
        fleaseconds += POP
##    score_msg = 'Score: ' + str(globscore)
    score_msg = 'Score: {:,}'.format(globscore)
    pop_msg = 'Population: ' + str(POP) + ' (max: ' + str(MAX_POP) + ')'
    bitten_msg = 'Bitten area: ' + str(bitten_area_percent) + ' %'
##    msg2screen('Power', (0,0,0,), font, screen, (5, 0), 'topleft')
    if dispmod > 0:
        msg2screen(score_msg, (0,0,0,), font, screen, (screen_width, 0))
    if dispmod == 2:
        msg2screen('Time: ' + str(time), (0,0,0,), font, screen, (half_width-120, 0), 'topleft')
        msg2screen('Fleatime: ' + str(fleaseconds), (0,0,0,), font, screen, (half_width, 0), 'topleft')
        msg2screen(bitten_msg, (0,0,0,), font, screen, (screen_width, 25))
        msg2screen(pop_msg, (0,0,0,), font, screen, (screen_width - 150, 0))
    
    if GAMEOVER :
        msg2screen("GAME OVER", (0,0,0,), gover_font, screen, (half_width, half_height-50), 'center')
        msg2screen("Press 'x' to start again", (0,0,0,), font, screen, (half_width, half_height), 'center')
        for event in pygame.event.get():
            if event.type == KEYDOWN and \
               event.key == K_x:
                initial_state()
        
    pygame.display.update()
    
    LAST_FPS = clock.get_fps()
##        print(LAST_FPS)
    clock.tick(fps)


pygame.quit()
##quit()


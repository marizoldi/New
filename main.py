### Added animation (explosions)

import pygame, random, time, sys
from pygame.locals import *

        # PYGAME SETUP AND INITIALISATION
pygame.init()

# -- Global constants
 
# COLOURS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
 
# Screen dimensions
SCREEN_WIDTH = 740
SCREEN_HEIGHT = 800
FPS = 30

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Space Invaders with Sprites!")
clock = pygame.time.Clock()
font = pygame.font.SysFont('exo2',20)

# Loading images and converting where appropriate
img1 = pygame.image.load("Assets/ship.png")
img1.set_colorkey((255,255,255))
img2 = pygame.image.load("Assets/enemy2_1.png").convert_alpha()
background = pygame.image.load("Assets/background.jpg").convert()
background2 = pygame.image.load("Assets/sidpt2.png").convert()
background2.set_colorkey((0,0,0))

explosions = []

# Load images in a list for explosion animation
for i in range(9):
    filename = 'Assets/regularExplosion0{}.png'.format(i)
    explosion_image = pygame.image.load(filename).convert()
    explosion_image.set_colorkey(BLACK)
    exp_img = pygame.transform.scale(explosion_image, (32,32))
    explosions.append(exp_img)


w,h = background.get_size()
y = 0
y1 = -h

last_missile_spawned = 0

## CLASS DECLERATIONS ##

class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = img1
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.bottom = SCREEN_HEIGHT - self.rect.y - 100
        self.speedx = 3
        self.lives = 2

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()

        if keystate[K_LEFT]:
            self.speedx = -5
        if keystate[K_RIGHT]:
            self.speedx = 5

        self.rect.x += self.speedx

        if self.rect.right > 500:
            self.rect.right = 500
        if self.rect.left < 200:
            self.rect.left = 200


    def shoot(self):
        b = Missile(self.rect.centerx - 11, self.rect.top, -5)
        fighterMissiles.add(b)
        all_sprites_list.add(b)



class Invader(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img2
        self.image2 = img2
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.xspeed = 1
        self.timer = pygame.time.get_ticks()
        

    def shoot(self):
        b = Missile(self.rect.centerx - 10, self.rect.bottom - 22, 2)
        invaderMissiles.add(b)
        all_sprites_list.add(b)
                

    def update(self):
        self.rect.x += self.xspeed

        if moveDown:
            self.rect.y += 5


class Missile(pygame.sprite.Sprite):

    def __init__(self,x,y,yDir):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([4, 6])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.yspeed = yDir
        # pygame.draw.line(self.image, (255,0,0), (0, 0), (4, 6), 4)

    def update(self):
        self.rect.y += self.yspeed
        if self.rect.top < 0:
            self.kill()


class Explosions(pygame.sprite.Sprite):

    def __init__(self, center):

        pygame.sprite.Sprite.__init__(self)
        self.image = explosions[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.pose = 0
        self.current_frame = 0
        self.frames_between = 3
         

    def update(self):

        self.current_frame += 1
        
        if self.current_frame >= self.frames_between:  
            old_center = self.rect.center
            self.pose = self.pose + 1 
            if self.pose == len(explosions) - 1:
                self.kill()
            else:
                self.image = explosions[self.pose]
                self.rect = self.image.get_rect()
                self.rect.center = old_center
                self.current_frame = 0
                


def show_restart_screen():

    waiting = True
     
    while waiting:
        screen.fill(BLACK)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
            if event.type == pygame.KEYUP:   
                waiting = False
           

def rollingBackgrd():
    global y,y1,h
    screen.blit(background,(0,y))
    screen.blit(background,(0,y1))
    y += 1
    y1 += 1

    if y > h:
        y = -h
    if y1 > h:
        y1 = -h


## INSTANTIATIONS / GLOBAL VARIABLES 

player = Player()

all_sprites_list = pygame.sprite.Group()
invaders = pygame.sprite.Group()
fighterMissiles = pygame.sprite.Group()
invaderMissiles = pygame.sprite.Group()
all_sprites_list.add(player)

def spawnInvaders():
    # Creating the invaders
    for i in range(240,360,40):
        for j in range(100,500,50):
            e = Invader(j, i)
            invaders.add(e)
            all_sprites_list.add(e)

spawnInvaders()

gameOn = True
reverse = False
moveDown = False

## MAIN LOOP
while gameOn:


    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
            gameOn = False
        elif event.type == pygame.KEYDOWN and event.key == K_SPACE:
                player.shoot()
    

    all_sprites_list.update()   
    
    if pygame.sprite.spritecollide(player, invaders, True, pygame.sprite.collide_mask) or \
    pygame.sprite.spritecollide(player,invaderMissiles, True, pygame.sprite.collide_mask):
        if player.lives <= 3 and player.lives > 1:
            player.lives -= 1
             
        else:
            screen.fill(BLACK)
            screen.blit(font.render("Lives: " + "0", True, (0,255,0)), (10,5))
            pygame.display.flip()

            show_restart_screen()
            player.lives = 4
            all_sprites_list = pygame.sprite.Group()
            invaders = pygame.sprite.Group()
            fighterMissiles = pygame.sprite.Group()
            invaderMissiles = pygame.sprite.Group()
            player = Player()
            all_sprites_list.add(player)

            spawnInvaders()

    screen.fill(BLACK)

    hits = pygame.sprite.groupcollide(invaders, fighterMissiles, True, True)
    hitsMissile = pygame.sprite.groupcollide(fighterMissiles, invaderMissiles, True, True)

    for inv in invaders:

        if inv.rect.right > 650 or inv.rect.left < 100:
            reverse = True  

    if len(invaders.sprites()) != 0:
        if pygame.time.get_ticks() - last_missile_spawned > 1200:
            random.choice(invaders.sprites()).shoot()
            last_missile_spawned = pygame.time.get_ticks()

        if pygame.time.get_ticks() - last_missile_spawned > 700:
            random.choice(invaders.sprites()).shoot()
            last_missile_spawned = pygame.time.get_ticks()


    # Check for collision with window screen on both sides
    if reverse:
        for i in invaders:
            i.xspeed *= -1
        reverse = False
        moveDown = True
        invaders.update()


    moveDown = False

    invaders.update()
         

    for hit in hits:
        ex = Explosions(hit.rect.center)
        all_sprites_list.add(ex)
    
    all_sprites_list.update()   

    rollingBackgrd()
    screen.blit(background2, (0,0))
    screen.blit(font.render("Lives: " + str(player.lives), True, (0,255,0)), (10,5))
         
    all_sprites_list.draw(screen)

    pygame.display.flip()




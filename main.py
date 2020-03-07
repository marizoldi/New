### Added animation (explosions)

import pygame, random, time, sys
from pygame.locals import *

        # PYGAME SETUP AND INITIALISATION
pygame.init()

# -- Global constants
 
# COLOURS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
 
# Screen dimensions
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 400
FPS = 70

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Space Invaders with Sprites!")
clock = pygame.time.Clock()
font = pygame.font.SysFont('exo2',20)

# Loading images and converting where appropriate
img1 = pygame.image.load("fighter.png")
img1.set_colorkey((255,255,255))
img2 = pygame.image.load("invader.png").convert_alpha()
img3 = pygame.image.load("missile.png").convert_alpha()
background = pygame.image.load("background.jpg").convert()

explosions = []

# Load images in a list for explosion animation
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    explosion_image = pygame.image.load(filename).convert()
    explosion_image.set_colorkey(BLACK)
    exp_img = pygame.transform.scale(explosion_image, (32,32))
    explosions.append(exp_img)


w,h = background.get_size()
y = 0
y1 = -h


## CLASS DECLERATIONS ##

class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = img1
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.bottom = SCREEN_HEIGHT - self.rect.y - 2
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

        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


    def shoot(self):
        b = Bullet(self.rect.centerx - 11, self.rect.top)
        bullets.add(b)
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
        # self.yspeed = 1
        self.xspeed = 1
        self.last_update = pygame.time.get_ticks()

    def update(self):
        # self.rect.y += self.yspeed
        self.rect.x += self.xspeed

        if self.last_update - pygame.time.get_ticks() > 70:
            self.last_update = pygame.time.get_ticks()

        # if self.rect.top > SCREEN_HEIGHT:
        #   self.rect.x = random.randint(0,800)
        #   self.rect.y = 0
        #   self.yspeed = random.randint(1,2)
        #   self.xspeed = random.randint(-2,2)


class Bullet(pygame.sprite.Sprite):

    def __init__(self,x,y):

        pygame.sprite.Sprite.__init__(self)
        self.image = img3
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.yspeed = -5

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
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == K_ESC:
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
bullets = pygame.sprite.Group()
all_sprites_list.add(player)

# Creating the invaders
for i in range(40,160,33):
    for j in range(100,500,50):
        e = Invader(j, i)
        invaders.add(e)
        all_sprites_list.add(e)

gameOn = True
reverse = False

## MAIN LOOP
while gameOn:

    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
            gameOn = False
        elif event.type == pygame.KEYDOWN and event.key == K_SPACE:
                player.shoot()
        # elif event.type == ADDENEMY:
        #   addEnemy()
    

    all_sprites_list.update()   
    
    if pygame.sprite.spritecollide(player, invaders, True, pygame.sprite.collide_mask):
        if player.lives <= 3 and player.lives > 1:
            player.lives -= 1
            addInvader()
        else:
            screen.fill(BLACK)
            # screen.blit(font.render("Lives: " + "0", True, (0,255,255)), (5,5))
            pygame.display.flip()

            show_restart_screen()
            all_sprites_list = pygame.sprite.Group()
            invaders = pygame.sprite.Group()
            bullets = pygame.sprite.Group()
            player = Player()
            all_sprites_list.add(player)

            for i in range(6):
                e = Invader()
                invaders.add(e)
                all_sprites_list.add(e)

    hits = pygame.sprite.groupcollide(invaders, bullets, True, True)

    for inv in invaders:
        if inv.rect.right > SCREEN_WIDTH or inv.rect.left < 0:
            reverse = True
            # print("reversed")

    if reverse:
        print("here")
        for i in invaders:
            i.xspeed *= -1
        reverse = False

    
    invaders.update()
         

    for hit in hits:
        ex = Explosions(hit.rect.center)
        all_sprites_list.add(ex)
    
    screen.fill(BLACK)
    rollingBackgrd()
    # screen.blit(font.render("Lives: " + str(player.lives), True, (0,255,255)), (5,5))
         
    all_sprites_list.draw(screen)

    pygame.display.flip()










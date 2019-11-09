import pygame, sys, random, math, time
from pygame.locals import *

# pygame.mixer.pre_init(44100, -16, 2, 2048)

pygame.init()
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

background = pygame.image.load('background.jpg')

# This function will create a display Surface
screen = pygame.display.set_mode(background.get_size())

spaceship = pygame.image.load("spaceship.png").convert_alpha()
enemy_image1 = pygame.image.load("invader.png").convert_alpha()
enemy_image = pygame.transform.scale(enemy_image1, (35, 35))


last_time_enemy_spawned = 0
time_since_last_shot = 0
BLACK = (0, 0, 0)

score = 0
lives = 4


class Enemies(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 800)
        self.rect.y = 0
        self.yspeed = random.randint(1, 2)
        self.xspeed = random.randint(-2, 2)
        self.dx = 1

    def update(self):
        self.rect.y += self.yspeed
        self.rect.x += self.xspeed

        if self.rect.top > background.get_size()[1]:
            self.rect.x = random.randint(0, 800)
            self.rect.y = 0
            self.yspeed = random.randint(1, 2)
            self.xspeed = random.randint(-2, 2)

        if self.rect.right > 800 or self.rect.left < 0:
            self.xspeed *= -1



class Fighter(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = spaceship
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = background.get_size()[0] / 2
        self.rect.bottom = background.get_size()[1] - self.rect.y - 2
        self.speedx = 3
        self.lives = 5
        self.angle = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()

        if keystate[K_LEFT]:
            self.speedx = -5
        if keystate[K_RIGHT]:
            self.speedx = 5

        self.rect.x += self.speedx

        if self.rect.right > background.get_size()[0]:
            self.rect.right = background.get_size()[0]
        if self.rect.left < 0:
            self.rect.left = 0

    def fire(self):
        b = Bullet(self.rect.centerx, self.rect.top)
        bullets.add(b)
        all_sprites_list.add(b)

    # def hit_by(self, enemy):
    #     return pygame.Rect(self.x, self.y, 50, 50).collidepoint(enemy.x, enemy.y + 20)


class Missile(pygame.sprite.Sprite):

    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.draw.line(screen, (255, 0, 0), (self.x, self.y), (self.x, self.y - 4), 1)
        self.rect.x = x
        self.rect.y = y
        self.yspeed = -5

    def update(self):
        self.rect.y += self.yspeed



fighter = Fighter()


all_sprites_list = pygame.sprite.Group()
enemies = pygame.sprite.Group()
missiles = pygame.sprite.Group()
all_sprites_list.add(fighter)


gameOn = True

while gameOn:

    # EXIT PROCESS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOn = False
        if event.type == pygame.KEYDOWN:
            if event.key == K_SPACE:
                fighter.fire()

    pressed_keys = pygame.key.get_pressed()

    if pressed_keys[K_ESCAPE]:
        sys.exit()



    if time.time() - last_time_enemy_spawned > 0.8:
        enemies.add(Enemies())
        # all_sprites_list.add(e)
        last_time_enemy_spawned = time.time()

    if pressed_keys[K_SPACE] and time.time() - time_since_last_shot > 0.2:
        fighter.fire()
        time_since_last_shot = time.time()

    all_sprites_list.update()
    enemies.update()
    missiles.update()

    # RENDER PROCESS
    screen.fill(BLACK)
    all_sprites_list.draw(screen)

    ######## rollingBackgrd()




    pygame.display.flip()


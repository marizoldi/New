import pygame, random, time, sys
from pygame.locals import *

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
fontS = pygame.font.SysFont('spaceinvaders', 30)
# fontM = pygame.font.SysFont('itcmachinestd',20)

# Loading images and converting where appropriate
img1 = pygame.image.load("Assets/ship.png")
img1.set_colorkey((255, 255, 255))
background = pygame.image.load("Assets/background.jpg").convert()
background2 = pygame.image.load("Assets/sidpt2.png").convert()
background2.set_colorkey((0, 0, 0))
startScreen = pygame.image.load("Assets/startScreen.jpg").convert()

enemy1 = []
enemy2 = []
enemy3 = []
explosions = []

# Load images in a list for explosion animation
for i in range(9):
    filename = 'Assets/regularExplosion0{}.png'.format(i)
    explosion_image = pygame.image.load(filename).convert()
    explosion_image.set_colorkey(BLACK)
    exp_img = pygame.transform.scale(explosion_image, (32, 32))
    explosions.append(exp_img)

# Load enemy 1 in a list for  animation
for i in range(1, 3):
    filename = 'Assets/enemy1_{}.png'.format(i)
    enemy_image = pygame.image.load(filename).convert_alpha()
    enemy1.append(enemy_image)
# Load enemy 2 in a list for  animation
for i in range(1, 3):
    filename = 'Assets/enemy2_{}.png'.format(i)
    enemy_image = pygame.image.load(filename).convert_alpha()
    enemy2.append(enemy_image)
# Load enemy 3 in a list for  animation
for i in range(1, 3):
    filename = 'Assets/enemy3_{}.png'.format(i)
    enemy_image = pygame.image.load(filename).convert_alpha()
    enemy3.append(enemy_image)


## CLASS DECLERATIONS ##

class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = img1
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.bottom = SCREEN_HEIGHT - self.rect.y - 100
        self.speedx = 3
        self.lives = 4

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()

        if keystate[K_LEFT]:
            self.speedx = -5
        if keystate[K_RIGHT]:
            self.speedx = 5

        self.rect.x += self.speedx

        if self.rect.right > 600:
            self.rect.right = 600
        if self.rect.left < 200:
            self.rect.left = 200

    def shoot(self):
        b = Missile(self.rect.centerx - 11, self.rect.top, -5)
        fighterMissiles.add(b)
        all_sprites_list.add(b)


class Invader(pygame.sprite.Sprite):

    def __init__(self, x, y, invIm):
        pygame.sprite.Sprite.__init__(self)
        self.image = invIm[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.xspeed = 1
        self.invIm = invIm
        self.pose = 0
        self.current_frame = 0
        self.last_time = time.time()

    def shoot(self):
        b = Missile(self.rect.centerx - 10, self.rect.bottom - 22, 8)
        invaderMissiles.add(b)
        all_sprites_list.add(b)

    def update(self):
        self.rect.x += self.xspeed

        if moveDown:
            if level == 1:
                self.rect.y += 5
            elif level == 2:
                self.rect.y += 25
            elif level == 3:
                self.rect.y += 35
        # Animating sprites. Only two frames so can implement it this way
        if self.current_frame == 0 and time.time() - self.last_time > FPS / 100:
            self.current_frame = 1
            self.last_time = time.time()
            self.image = self.invIm[self.current_frame]
        elif self.current_frame == 1 and time.time() - self.last_time > FPS / 100:
            self.current_frame = 0
            self.last_time = time.time()
            self.image = self.invIm[self.current_frame]


class Missile(pygame.sprite.Sprite):

    def __init__(self, x, y, yDir):
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


# INSTANTIATIONS / GLOBAL VARIABLES
all_sprites_list = pygame.sprite.Group()
invaders = pygame.sprite.Group()
fighterMissiles = pygame.sprite.Group()
invaderMissiles = pygame.sprite.Group()
invaders10 = pygame.sprite.Group()
invaders20 = pygame.sprite.Group()
invaders30 = pygame.sprite.Group()
player = Player()
all_sprites_list.add(player)

w, h = background.get_size()
y = 0
y1 = -h

last_missile_spawned = 0
level = 1
gameOn = True
reverse = False
moveDown = False
start = True
restart = False
won = False
score = 0


def start_screen():
    global start
    global restart
    global won
    waiting = True
    print("here")

    screen.fill(BLACK)
    if start:
        screen.blit(startScreen, (50, 0))
        pygame.draw.rect(screen, (120, 120, 120, 60), (140, 340, 470, 55))
        pygame.draw.rect(screen, GREEN, (140, 340, 470, 55), 3)
        screen.blit(fontS.render("Press Enter to start", True, (0, 235, 0)), (170, 350))
        start = False
    if restart:
        screen.blit(fontS.render("Game Over", True, (0, 255, 0)), (100, 250))
        screen.blit(fontS.render("Press Enter to restart", True, (0, 235, 0)), (100, 300))
        restart = False
    if won:
        screen.blit(fontS.render("You WON!", True, (0, 255, 0)), (100, 250))
        screen.blit(fontS.render("All Space Invaders are destroyed", True, (0, 255, 0)), (100, 300))
        screen.blit(fontS.render("Press Enter to play again", True, (0, 235, 0)), (100, 350))
        won = False
        start = True

    pygame.display.update()

    while waiting:
        for myevent in pygame.event.get():
            if myevent.type == pygame.QUIT or (myevent.type == pygame.KEYDOWN and myevent.key == K_ESCAPE):
                sys.exit()
            if myevent.type == pygame.KEYDOWN and myevent.key == K_RETURN:
                waiting = False


def rollingBackgrd():
    global y, y1, h
    screen.blit(background, (0, y))
    screen.blit(background, (0, y1))
    y += 1
    y1 += 1

    if y > h:
        y = -h
    if y1 > h:
        y1 = -h


def spawnInvaders():
    # Creating the 30 point invaders
    for i in range(240, 320, 40):
        for j in range(100, 500, 50):
            e = Invader(j, i, enemy1)
            invaders30.add(e)
            invaders.add(e)
            all_sprites_list.add(e)
    # Creating the 20 point invaders
    for i in range(320, 400, 40):
        for j in range(100, 500, 50):
            e = Invader(j, i, enemy2)
            invaders20.add(e)
            invaders.add(e)
            all_sprites_list.add(e)
    # Creating the 10 point invaders
    for i in range(400, 480, 40):
        for j in range(100, 500, 50):
            e = Invader(j, i, enemy3)
            invaders10.add(e)
            invaders.add(e)
            all_sprites_list.add(e)


spawnInvaders()

## MAIN LOOP
while gameOn:

    clock.tick(FPS)

    if start:
        start_screen()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
            gameOn = False
        elif event.type == pygame.KEYDOWN and event.key == K_SPACE:
            player.shoot()

    if pygame.sprite.spritecollide(player, invaders, True) or pygame.sprite.spritecollide(player, invaderMissiles,
                                                                                          True):
        if 4 >= player.lives > 1:
            player.lives -= 1
        # Game Over and restart screen
        else:
            restart = True
            start_screen()
            all_sprites_list = pygame.sprite.Group()
            invaders = pygame.sprite.Group()
            fighterMissiles = pygame.sprite.Group()
            invaderMissiles = pygame.sprite.Group()
            invaders10 = pygame.sprite.Group()
            invaders20 = pygame.sprite.Group()
            invaders30 = pygame.sprite.Group()
            player = Player()
            all_sprites_list.add(player)
            score = 0
            player.lives = 4
            spawnInvaders()

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

    elif level < 2:
        level += 1
        all_sprites_list = pygame.sprite.Group()
        invaders = pygame.sprite.Group()
        invaders10 = pygame.sprite.Group()
        invaders20 = pygame.sprite.Group()
        invaders30 = pygame.sprite.Group()
        all_sprites_list.add(player)
        spawnInvaders()
    else:
        won = True
        start_screen()
        all_sprites_list = pygame.sprite.Group()
        invaders = pygame.sprite.Group()
        fighterMissiles = pygame.sprite.Group()
        invaderMissiles = pygame.sprite.Group()
        invaders10 = pygame.sprite.Group()
        invaders20 = pygame.sprite.Group()
        invaders30 = pygame.sprite.Group()
        player = Player()
        all_sprites_list.add(player)
        score = 0
        player.lives = 4
        spawnInvaders()

    # Check for collision with window screen on both sides
    if reverse:
        for i in invaders:
            i.xspeed *= -1
            moveDown = True

        invaders.update()
        moveDown = False
        reverse = False
    # Need False, False here as we don't want to delete them before the next if clause
    hits = pygame.sprite.groupcollide(invaders, fighterMissiles, False, False)
    for hit in hits:
        ex = Explosions(hit.rect.center)
        all_sprites_list.add(ex)

    if pygame.sprite.groupcollide(invaders10, fighterMissiles, True, True):
        score += 10
    if pygame.sprite.groupcollide(invaders20, fighterMissiles, True, True):
        score += 20
    if pygame.sprite.groupcollide(invaders30, fighterMissiles, True, True):
        score += 30

    pygame.sprite.groupcollide(fighterMissiles, invaderMissiles, True, True)

    all_sprites_list.update()

    # RENDERING PROCESS
    screen.fill(BLACK)

    rollingBackgrd()
    screen.blit(background2, (0, 0))
    screen.blit(fontS.render("Lives: " + str(player.lives), True, (0, 255, 0)), (12, 5))
    screen.blit(fontS.render("Score: " + str(score), True, (0, 255, 0)), (12, 35))

    all_sprites_list.draw(screen)

    pygame.display.flip()
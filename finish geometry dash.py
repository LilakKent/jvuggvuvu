import pygame as pg

window = pg.display.set_mode((800, 600))
fon = pg.transform.scale(pg.image.load('fon.jpg'), (800, 600))
fon1 = pg.transform.scale(pg.image.load('fon.jpg'), (800, 600))
lose = pg.transform.scale(pg.image.load('gameover.jpg'), (800, 600))
zol = pg.transform.scale(pg.image.load('treasure.png'), (50, 50))
win = pg.transform.scale(pg.image.load('win.png'), (800, 600))
fon2 = pg.transform.scale(pg.image.load('win2.jpg'), (50, 1200))
pg.init()


class Config:
    FPS = 40
    ABS_JUMP_COUNT = 30
    JUMP_COUNT_ACCEL = 1
    GENERAL_SPEED = 7


zol_x = 2200
zol_y = 620

fon_x = 0

fon1_x = 800

run = True
clock = pg.time.Clock()
finish = False

class FinalSprite(pg.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(pg.image.load(player_image), (800, 600))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = Config.GENERAL_SPEED

    def update(self):
        self.rect.x -= self.speed
        window.blit(self.image, (self.rect.x, self.rect.y))
        if self.rect.x < 0:
            blocks.remove(self)

class Treasure(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = zol
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.speed = Config.GENERAL_SPEED

    def update(self):
        self.rect.x -= self.speed
        window.blit(self.image, (self.rect.x, self.rect.y))
        if self.rect.x < - 100:
            treasures.remove(self)


class Hero(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load('Cube.png'), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.y_speed = 0
        self.score = 0
        self.stands_on = False

    def collect(self):
        self.score += 1

    def gravitate(self):
        self.y_speed += Config.JUMP_COUNT_ACCEL

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def jump(self):
        self.y_speed -= Config.ABS_JUMP_COUNT

    def collide(self):
        for collided_block in pg.sprite.spritecollide(self, blocks, False):
            if collided_block.rect.center[1] > self.rect.center[1]:
                self.stands_on = True
                self.rect.bottom = collided_block.rect.top
                break
            elif self.y_speed < 0:
                self.y_speed = 0
        else:
            self.stands_on = False

    def update(self):
        self.collide()

        self.gravitate()

        if self.stands_on and self.y_speed > 0:
            self.y_speed = 0
        elif self.rect.y <= 0 and self.y_speed < 0:
            self.rect.y = 0
            self.y_speed = 0
        else:
            self.rect.y += self.y_speed

        self.reset()


class Block(pg.sprite.Sprite):
    def __init__(self, width, y, x=800):
        super().__init__()
        self.width = width
        self.speed = Config.GENERAL_SPEED
        self.height = 30
        self.image = pg.Surface((self.width, self.height))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

    def update(self):
        self.rect.x -= self.speed
        window.blit(self.image, (self.rect.x, self.rect.y))
        if self.rect.x + self.width < 0:
            blocks.remove(self)


blocksscor = [(400, 500, 200),
              (500, 400, 900,),
              (500, 200, 1600),
              (500, 580, 1900),
              (500, 350, 2300),
              (500, 600, 2200),
              (500, 580, 2700),
              (500, 200, 3200),
              (500, 350, 3900)]
treasures_cors = [
    (400, 430),
    (1200, 330)
]

blocks = pg.sprite.Group()
treasures = pg.sprite.Group()
for t in treasures_cors:
    treasures.add(Treasure(*t))
for b in blocksscor:
    blocks.add(Block(*b))

dash = Hero(100, 100)
font = pg.font.SysFont('Calibri', 25, True, False)
pg.mixer.init()
pg.mixer.music.load('BaseAfterBase.ogg')
pg.mixer.music.play()

final = FinalSprite('win2.jpg',4150, 350)
blocks.add(final)

while run:
    window.blit(fon1, (fon1_x, 0))
    window.blit(fon, (fon_x, 0))
    window.blit(zol, (zol_x, zol_y))
    window.blit(fon2, (4150, 350))	
    dash.update()

    blocks.update()
    treasures.update()

    events = pg.event.get()

    fon_x -= Config.GENERAL_SPEED
    fon1_x -= Config.GENERAL_SPEED
    if fon_x <= -800:
        fon_x = 800
    if fon1_x <= -800:
        fon1_x = 800

    for event in events:
        if event.type == pg.QUIT:
            run = False

    keys_pressed = pg.key.get_pressed()

    if keys_pressed[pg.K_SPACE] and dash.stands_on:
        dash.jump()

    if dash.rect.y >= 620:
        window.blit(lose, (0, 0))

    if pg.sprite.collide_rect(dash, final):
        window.blit(win, (0,0))
        finish = True
        run = False
        

    if pg.sprite.spritecollide(dash, treasures, True):
        dash.collect()
    text = font.render("Score: " + str(dash.score), True, (0, 0, 0))
    window.blit(text, (10, 10))




    clock.tick(Config.FPS)

    pg.display.update()

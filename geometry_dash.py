import pygame as pg
window = pg.display.set_mode((800, 600))
fon = pg.transform.scale(pg.image.load('fon.jpg'), (800, 600))
fon1 = pg.transform.scale(pg.image.load('fon.jpg'), (800, 600))

class Config:
    FPS = 40
    ABS_JUMP_COUNT = 10
    JUMP_COUNT_ACCEL = 1
    GENERAL_SPEED = 4

fon_x = 0

fon1_x = 800

dash_y = 500

dash = pg.transform.scale(pg.image.load('Cube.png'), (100, 100))
isJump = False
jumpCount = Config.ABS_JUMP_COUNT
run = True
clock = pg.time.Clock()

class Block(pg.sprite.Sprite):
    def __init__(self,width,y,x = 800):
        super().__init__()
        self.width = width
        self.speed = Config.GENERAL_SPEED
        print(width)
        self.height = 10
        self.image = pg.Surface((self.width,self.height))
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
    def update(self):
        self.rect.x -= self.speed
        window.blit(self.image, (self.rect.x,self.rect.y))
        if self.rect.x + self.width < 0:
            blocks.remove(self)
blocksscor = [(800,500,0),
    (500,400,900,),
    (500,200,1600)]
blocks = pg.sprite.Group()
for b in blocksscor:
    blocks.add(Block(*b))


while run:
    window.blit(fon1, (fon1_x,0))
    window.blit(fon, (fon_x,0))
    window.blit(dash, (0, dash_y))
    print(blocks)
    blocks.update()

    events = pg.event.get()
    
    
    fon_x -= Config.GENERAL_SPEED
    fon1_x -= Config.GENERAL_SPEED
    if fon_x == -800:
        fon_x = 800
    if fon1_x == -800:
        fon1_x = 800

    for event in events:
        if event.type == pg.QUIT:
            run = False
    
    keys_pressed = pg.key.get_pressed()


    if keys_pressed[pg.K_SPACE]:
        isJump = True 
    if isJump and jumpCount >= -Config.ABS_JUMP_COUNT:
        if jumpCount < 0:
            dash_y += (jumpCount ** 2 ) / 2
        else:
            dash_y -= (jumpCount ** 2) / 2
        jumpCount -= Config.JUMP_COUNT_ACCEL
    else:
        isJump = False
        jumpCount = Config.ABS_JUMP_COUNT


    clock.tick(Config.FPS)

    pg.display.update()

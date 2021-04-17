import pygame as pg
window = pg.display.set_mode((800, 600))
fon = pg.transform.scale(pg.image.load('fon.jpg'), (800, 600))
fon1 = pg.transform.scale(pg.image.load('fon.jpg'), (800, 600))

x = 0
y = 0

x1 = 800

y1 = 500

dash = pg.transform.scale(pg.image.load('Cube.png'), (100, 100))
isJump = False
jumpCount = 10
run = True
clock = pg.time.Clock()


class Enemy:
    direction = 'forward'
    distance = 800
    def update():
        if x - x >= 0:
            self.direction = 'forward'
        elif self.direction == 'forward':
            x += self.spweed

while run:
    window.blit(fon1, (x1,0))
    window.blit(fon, (x,0))
    window.blit(dash, (0, y1))

    events = pg.event.get()
    

    x -= 1
    x1 -= 1
    if x == -800:
        x = 800
    if x1 == -800:
        x1 = 800

    for event in events:
        if event.type == pg.QUIT:
            run = False
    keys_pressed = pg.key.get_pressed()
    if keys_pressed[pg.K_SPACE]:
        isJump = True 
        if jumpCount >= -10:
            if jumpCount < 0:
                y1 += (jumpCount ** 2 ) / 2
            else:
                y1 -= (jumpCount ** 2) / 2
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10




    pg.display.update()

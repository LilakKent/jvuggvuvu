import pygame as pg
window = pg.display.set_mode((800, 600))
fon = pg.transform.scale(pg.image.load('fon.jpg'), (800, 600))
fon1 = pg.transform.scale(pg.image.load('fon.jpg'), (800, 600))
lose = pg.transform.scale(pg.image.load('gameover.jpg'), (800, 600))
zol = pg.transform.scale(pg.image.load('treasure.png'), (50, 50))
win = pg.transform.scale(pg.image.load('win.png'), (800, 600))

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

class Hero(pg.sprite.Sprite):
	def __init__(self, x, y):
		self.image = pg.transform.scale(pg.image.load('Cube.png'), (50, 50))
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.x = x
		self.y_speed = 0
		self.stands_on = False

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
		else:
			self.stands_on = False

	def update(self):
		self.collide()

		self.gravitate()

		if self.stands_on and self.y_speed > 0:
			self.y_speed = 0 
		else:
			self.rect.y += self.y_speed

		self.reset()

class Block(pg.sprite.Sprite):
	def __init__(self,width,y,x = 800):
		super().__init__()
		self.width = width
		self.speed = Config.GENERAL_SPEED
		self.height = 30
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

blocksscor = [(400,500,200),
	(500,400,900,),
	(500,200,1600),
	(500,580,1900),
	(500,350,2300),
	(500,600,2200),
	(500,580,2700),
	(500,200,3200),
	(500,350,4000)]
blocks = pg.sprite.Group()
for b in blocksscor:
	blocks.add(Block(*b))

dash = Hero(100, 100)


#pg.mixer.init()
#pg.mixer.music.load('BaseAfterBase.ogg')
#pg.mixer.music.play()

while run:
	window.blit(fon1, (fon1_x,0))
	window.blit(fon, (fon_x,0))
	window.blit(zol, (zol_x,zol_y))
	dash.update()



	blocks.update()

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

	if dash.rect.x >= 4000:
		window.blit(win, (0,0))



	clock.tick(Config.FPS)

	pg.display.update()

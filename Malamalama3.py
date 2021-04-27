import pygame, sys, os
from pygame import *
from pygame.locals import *
from colors import *

windowWidth = 600
windowHeight = 600
half_windowWidth = windowWidth/2
half_windowHeight = windowHeight/2

Window = (windowWidth, windowHeight)

DEPTH = 0
FLAGS = SRCALPHA

DEBUG = False

Levels = {
0 : [
"XXXXXXXXXXXXXXXXXXXX",
"X          XEX     X",
"X          X X     X",
"X          X X     X",
"X          X X     X",
"X          X X     X",
"X          X X     X",
"X          X X     X",
"XXXXXXXXXXXX XXXXXXX",
"XS                BX",
"XXXXXXXXXXXXXXXXXXXX",
"X                  X",
"X                  X",
"X                  X",
"X                  X",
"X                  X",
"X                  X",
"X                  X",
"X                  X",
"XXXXXXXXXXXXXXXXXXXX"
], 
1 : [
"XXXXXXXXXXXXXXXXXXXX",
"X    BX      X     X",
"X XXXXX      X XXX X",
"X X          X X X X",
"X X          XEX X X",
"X XXXXXXXXXXXXXXXX X",
"X                  X",
"X XXXXXXXXXXXXXXXX X",
"X X              X X",
"X X              X X",
"X X              X X",
"X XXXXXXXXXXXXXXXX X",
"X                  X",
"XXXXXXXXXXX XXXXXXXX",
"X         X X      X",
"X         X X      X",
"X         X X      X",
"X         X X      X",
"X         XSX      X",
"XXXXXXXXXXXXXXXXXXXX"
],
2 : [
"XXXXXXXXXXXXXXXXXXXX",
"X                  X",
"X                  X",
"XXXXXXXXXXXXXXXXXXXX",
"X             S    X",
"X XXXXXXXXXXXXXXXX X",
"X X X    X   X   X X",
"X X X XX X X X   X X",
"X X X XX X X X   X X",
"X XXX XX X X X   X X",
"X X   XX X X X   X X",
"X X XXXX X X XXXXX X",
"X X X  X   X       X",
"X X XXXXXXXX XXXXXXX",
"XE  X      X X     X",
"XXXXX      X X     X",
"X          X X     X",
"X          X X     X",
"X          XBX     X",
"XXXXXXXXXXXXXXXXXXXX"
],
3 : [
"XXXXXXXXXXXXXXXXXXXX",
"X                 xX",
"X XXXXXXXXXXXXXXX XX",
"X X             X XX",
"X X             X XX",
"X X             X XX",
"X X             X XX",
"X X         XXXXX XX",
"X XXXXXXXXXXX     XX",
"X           X XXXXXX",
"XXXXXXXXXXX X      X",
"X         XBXXXXXX X",
"X         X X    X X",
"XXXXXXXXXXX XXXXXX X",
"XS                 X",
"X XXXXXXXXXXXXXXXXXX",
"X                  X",
"XXXXXXXXXXXXXXXXXX X",
"X                XEX",
"XXXXXXXXXXXXXXXXXXXX"
],
4 : [
"XXXXXXXXXXXXXXXXXXXX",
"XXX   BX           X",
"XXX XXXX           X",
"X      X           X",
"X X XX X           X",
"X X XX XXXX        X",
"XEX       X        X",
"XXXXXX XX X        X",
"X    X XX XXXX     X",
"X    X       X     X",
"X    XXXX XX X     X",
"X       X XX XXXX  X",
"X       X       X  X",
"X       XXXX XX X  X",
"X          X XX XXXX",
"X          X       X",
"X          X XX XX X",
"X    XXXXXXX XX XX X",
"X    XB      XX   SX",
"XXXXXXXXXXXXXXXXXXXX"
],
5 : [
"XXXXXXXXXXXXXXXXXXXX",
"X                  X",
"X XXXXXX XXXXXXXXX X",
"X X    X X       X X",
"X XXX  X X       X X",
"X X XXXX X       X X",
"XS       X       X X",
"X X XXXXXXXXXXXXXX X",
"X X                X",
"X X XXXXXXXXXXXXXXXX",
"X X                X",
"X XXXXXXXXXXXXXXXX X",
"X X      XB        X",
"X XXXXXXXXX XXXXXXXX",
"X XEX     X X      X",
"X X XXXXXXX XXXXXXXX",
"X X                X",
"X XXXXXXXXXXXXXXXX X",
"X                  X",
"XXXXXXXXXXXXXXXXXXXX"
]}

class Scene(object):
    def __init__(self):
        pass

    def render(self, screen):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def handle_events(self, events):
        raise NotImplementedError
		
class TitleScene(object):
	def __init__(self):
		super(TitleScene, self).__init__()
		self.font = pygame.font.SysFont('Arial', 56)
		self.sfont = pygame.font.SysFont('Arial', 32)

	def render(self, screen):
		screen.fill(black)
		text1 = self.font.render('Malamalama', True, (255, 255, 255))
		text2 = self.sfont.render('> press space to start <', True, (255, 255, 255))
		screen.blit(text1, (half_windowWidth - 160, 50))
		screen.blit(text2, (half_windowWidth - 160, 350))

	def update(self):
		pass

	def handle_events(self, events):
		for e in events:
			if e.type == KEYDOWN and e.key == K_SPACE:
				self.manager.go_to(GameScene(0))
				
class TransitionScene(Scene):
	def __init__(self, lvlNumber):
		super(TransitionScene, self).__init__()
		self.lvlNumber = lvlNumber

	def render(self, screen):
		screen.set_alpha

	def update(self):
		pass

	def handle_events(self):
		pass
				
class GameScene(Scene):
	def __init__(self, lvlNumber):
		super(GameScene, self).__init__()
		self.lvlNumber = lvlNumber		
		self.entities = pygame.sprite.Group()
		self.walls = []
		self.light = black
		self.buttonColor = black
		self.exitColor = black
		self.wallColor = black
		self.leave = False
		
		levels = Levels[lvlNumber]
		
		x = 0
		y = 0
		for row in levels:
			for col in row:
				if col == "X":
					w = Walls(x, y)
					self.walls.append(w)
					self.entities.add(w)
					w.image.fill(self.wallColor)
				if col == "B":
					w = Button(x, y)
					self.entities.add(w)
					w.image.fill(self.buttonColor)
				if col == "E":
					w = ExitBlock(x, y, self.leave)
					self.entities.add(w)
					w.image.fill(self.exitColor)
				if col == "S":
					self.playerX = x
					self.playerY = y
				x += 30
			y += 30
			x = 0
		
		self.player = Player(self.playerX, self.playerY)
		self.player.scene = self
		self.entities.add(self.player)
	
	def render(self, screen):
		screen.fill(self.light)
		for e in self.entities:
			screen.blit(e.image, (e.rect.x, e.rect.y))
		
	def update(self):
		pressed = pygame.key.get_pressed()
		up, down, left, right = [pressed[key] for key in (K_UP, K_DOWN, K_LEFT, K_RIGHT)]
		self.player.update(up, down, left, right, self.walls, self.entities)
			
	def exit(self):
		if self.lvlNumber + 1 in Levels:
			self.manager.go_to(GameScene(self.lvlNumber + 1))
		else:
			self.manager.go_to(EndScene())
		
	def handle_events(self, events):
		for e in events:
			if e.type == KEYDOWN and e.key == K_ESCAPE:
				self.manager.go_to(TitleScene())

class EndScene(Scene):
	def __init__(self):
		super(EndScene, self).__init__()
		self.font = pygame.font.SysFont('Arial', 56)
		self.sfont = pygame.font.SysFont('Arial', 32)
		self.tfont = pygame.font.SysFont('Arial', 20)

	def render(self, screen):
		screen.fill(black)
		text1 = self.font.render('Thanks for playing!', True, (255, 255, 255))
		text2 = self.sfont.render('End of Alpha Demo', True, (255, 255, 255))
		text3 = self.tfont.render('press esc', True, (white))
		screen.blit(text1, (half_windowWidth - 240, 50))
		screen.blit(text2, (half_windowWidth - 160, 350))
		screen.blit(text3, (half_windowWidth - 140, 390))
		
	def update(self):
		pass
	
	def handle_events(self, events):
		for e in events:
			if e.type == KEYDOWN and e.key == K_ESCAPE:
				sys.exit()
				
class SceneMananger(object):
    def __init__(self):
        self.go_to(TitleScene())

    def go_to(self, scene):
        self.scene = scene
        self.scene.manager = self
		
class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Player(Entity):
	def __init__(self, x, y):
		Entity.__init__(self)
		self.xVelocity = 0
		self.yVelocity = 0
		self.size = 15
		self.image = Surface((self.size,self.size))
		self.image.fill(white)
		self.image.convert()
		self.rect = Rect(x*self.size, y*self.size, self.size, self.size)
		self.rect.x = x
		self.rect.y = y
		self.speed = 6
		
	def update(self, up, down, left, right, walls, entities):
		if up:
			self.yVelocity = -self.speed
			self.xVelocity = 0
			#print "up"
		if down:
			self.yVelocity = self.speed
			self.xVelocity = 0
			#print "down"
		if left:
			self.xVelocity = -self.speed
			self.yVelocity = 0
			#print "left"
		if right:
			self.xVelocity = self.speed
			self.yVelocity = 0
			#print "right"
		if not (up or down or left or right):
			self.xVelocity = 0
			self.yVelocity = 0
		
		self.rect.left += self.xVelocity
		self.rect.top += self.yVelocity
		
		"""
		print "x velocity is: " + str(self.xVelocity)
		print "y velocity is: " + str(self.yVelocity)
		print "x position is: " + str(self.rect.x)
		print "y position is: " + str(self.rect.y)
		"""
		
		self.collide(self.xVelocity, self.yVelocity, walls)	
		self.special_collide(entities)

	def collide(self, xVelocity, yVelocity, walls):
		for w in walls:
			if pygame.sprite.collide_rect(self, w):
				if xVelocity > 0: 
					self.rect.right = w.rect.left
				if xVelocity < 0: 
					self.rect.left = w.rect.right
				if yVelocity > 0:
					self.rect.bottom = w.rect.top
				if yVelocity < 0:
					self.rect.top = w.rect.bottom
		return True
		
	def special_collide(self, entities):
		for i in entities:
			if pygame.sprite.collide_rect(self, i):
				if isinstance(i, Button) and self.scene.leave == False:
					#self.scene.light = pygame.image.load(os.path.join("C:\Users\Zach\Desktop\Python\Malamalama", "SandFloor.jpg"))
					self.scene.leave = True
					for e in self.scene.entities:
						if isinstance(e, Walls):
							e.image = pygame.image.load(os.path.join(".\images", "tree.jpg"))
						if isinstance(e, ExitBlock):
							e.image.fill(gold)
						if isinstance(e, Button):
							e.image.fill(red)
				if isinstance(i, ExitBlock) and self.scene.leave:
					self.scene.exit()
	
class Walls(Entity):
	def __init__(self, x, y):
		Entity.__init__(self)
		#self.image = Surface([32, 32], pygame.SRCALPHA, 32) #makes blocks invisible for much better artwork
		self.image = Surface((30,30)) #makes blocks visible for building levels
		self.image.fill(black)
		self.image.convert()
		self.rect = Rect(x, y, 30, 30)
		
class Button(Walls):
	def __init__(self, x, y):
		Walls.__init__(self, x, y)
		#self.image = Surface([32, 32], pygame.SRCALPHA, 32) #makes blocks invisible for much better artwork
		#self.image = Surface((30,30)) #makes blocks visible for building levels
		#self.image.fill(gold)
		#self.image.convert()
		#self.rect = Rect(x, y, 30, 30)
		
class ExitBlock(Walls):
	def __init__(self, x, y, active):
		Walls.__init__(self, x, y)
		self.active = active
		#self.image.fill(red)
		

def main():
    pygame.init()
    mixer.init()

    screen = pygame.display.set_mode(Window, FLAGS, DEPTH)
    pygame.display.set_caption("Malamalama Python 3.9")
    timer = pygame.time.Clock()
    running = True

    pygame.mixer.music.load(".\music\SadMalamalama.mp3")
    pygame.mixer.music.play(loops=-1)

    manager = SceneMananger()

    while running:
        timer.tick(60)

        if pygame.event.get(QUIT):
            running = False
            return
        manager.scene.handle_events(pygame.event.get())
        manager.scene.update()
        manager.scene.render(screen)
        pygame.display.flip()
		
		
if __name__ == "__main__":
    main()
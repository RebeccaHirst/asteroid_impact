import random
from sprites import *
from pygame.locals import *

# screens.py
class QuitGame(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class GameScreen():
	def __init__(self, screen, screenstack):
		self.screen = screen
		self.screenstack = screenstack
		self.opaque = True
		
	def update(self, millis):
		pass
	
	def draw(self):
		# TODO: fill entire screen with a unique color to indicate that draw() is being called here
		pass


class ClickToBeginOverlayScreen(GameScreen):
	def __init__(self, screen, gamescreenstack):
		GameScreen.__init__(self, screen, gamescreenstack)
		self.opaque = False
		self.screenarea = self.screen.get_rect()
		if pygame.font:
			self.font = load_font('freesansbold.ttf', 36)
			self.text = self.font.render("Click To Begin", 1, (250, 10, 10))
			self.textpos = self.text.get_rect(centerx=self.screenarea.width/2,centery=self.screenarea.height/2)

	def draw(self):
		self.screen.blit(self.text, self.textpos)
		pass

	def update(self, millis):
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key == K_ESCAPE:
				raise QuitGame('ESC Pressed')
			elif event.type == MOUSEBUTTONDOWN:
				self.screenstack.pop()
				pass
			elif event.type is MOUSEBUTTONUP:
				pass
				
		if len(self.screenstack) > 1 and isinstance(self.screenstack[-2], AsteroidImpactGameplayScreen):
			# update cursor:
			self.screenstack[-2].cursor.update(millis)

class GameOverOverlayScreen(GameScreen):
	def __init__(self, screen, gamescreenstack):
		GameScreen.__init__(self, screen, gamescreenstack)
		self.opaque = False
		self.screenarea = self.screen.get_rect()
		if pygame.font:
			self.font = load_font('freesansbold.ttf', 36)
			self.text = self.font.render("Game Over", 1, (250, 10, 10))
			self.textpos = self.text.get_rect(centerx=self.screenarea.width/2,centery=self.screenarea.height/2)

	def draw(self):
		self.screen.blit(self.text, self.textpos)
		pass

	def update(self, millis):
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key == K_ESCAPE:
				raise QuitGame('ESC Pressed')
			elif event.type == MOUSEBUTTONDOWN:
				self.screenstack.pop()
				if isinstance(self.screenstack[-1], AsteroidImpactGameplayScreen):
					self.screenstack.pop()
				# start game over
				self.screenstack.append(AsteroidImpactGameplayScreen(self.screen, self.screenstack))
				self.screenstack.append(ClickToBeginOverlayScreen(self.screen, self.screenstack))
			elif event.type is MOUSEBUTTONUP:
				pass

def circularspritesoverlap(a, b):
	x1 = a.rect.centerx
	y1 = a.rect.centery
	d1 = a.diameter
	x2 = b.rect.centerx
	y2 = b.rect.centery
	d2 = b.diameter
	# x1, y1, d1, x2, y2, d2
	return ((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1)) < (.25*(d1 + d2)*(d1 + d2))


class AsteroidImpactGameplayScreen(GameScreen):
	def __init__(self, screen, screenstack):
		GameScreen.__init__(self, screen, screenstack)
		self.screenarea = self.screen.get_rect()
		self.background = pygame.Surface(screen.get_size())
		self.background = self.background.convert()
		self.background.fill((250, 250, 250))

		if pygame.font:
			self.font = load_font('freesansbold.ttf', 36)
			text = self.font.render("Placeholder Art", 1, (10, 10, 10))
			textpos = text.get_rect(centerx=self.background.get_width()/2)
			self.background.blit(text, textpos)
			
		self.sound_death = load_sound('DeathFlash.wav')

		#Display The Background
		self.screen.blit(self.background, (0, 0))
		
		self.rnd = random.Random(3487437)
		self.cursor = Cursor()
		self.target = Target(diameter=16, left=self.rnd.randint(0, self.screenarea.width - 16), top=self.rnd.randint(0, self.screenarea.height - 16))
		self.asteroids = [Asteroid(diameter=100, dx=2, dy=5, top=100, left=10),
			Asteroid(diameter=80, dx=4, dy=3, top=200, left=50),
			Asteroid(diameter=60, dx=-5, dy=-3, top=120, left=400)]
		self.powerup_list = [
			ShieldPowerup(diameter=16, left=self.rnd.randint(0, self.screenarea.width - 16), top=self.rnd.randint(0, self.screenarea.height - 16)),
			SlowPowerup(diameter=16, left=self.rnd.randint(0, self.screenarea.width - 16), top=self.rnd.randint(0, self.screenarea.height - 16)),
			ShieldPowerup(diameter=16, left=self.rnd.randint(0, self.screenarea.width - 16), top=self.rnd.randint(0, self.screenarea.height - 16)),
			SlowPowerup(diameter=16, left=self.rnd.randint(0, self.screenarea.width - 16), top=self.rnd.randint(0, self.screenarea.height - 16)),
			ShieldPowerup(diameter=16, left=self.rnd.randint(0, self.screenarea.width - 16), top=self.rnd.randint(0, self.screenarea.height - 16)),	
			SlowPowerup(diameter=16, left=self.rnd.randint(0, self.screenarea.width - 16), top=self.rnd.randint(0, self.screenarea.height - 16)),
			]
		self.powerup = self.powerup_list[0]
		self.next_powerup_list_index = 1 % len(self.powerup_list)
		self.mostsprites = pygame.sprite.OrderedUpdates(self.asteroids + [self.cursor, self.target])
		self.powerupsprites = pygame.sprite.Group(self.powerup)

	def update(self, millis):
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key == K_ESCAPE:
				raise QuitGame('ESC Pressed')
			elif event.type == MOUSEBUTTONDOWN:
				pass
			elif event.type is MOUSEBUTTONUP:
				pass

		self.mostsprites.update(millis)
		# update powerups
		# if current power-up has been used completely:
		if self.powerup.used:
			# switch to and get ready next one:
			self.powerup = self.powerup_list[self.next_powerup_list_index]
			self.powerup.used = False
			print self.powerup.rect
			self.powerupsprites.empty()
			self.powerupsprites.add(self.powerup)
			self.next_powerup_list_index = (1 + self.next_powerup_list_index) % len(self.powerup_list)
		self.powerupsprites.update(millis)
		
		# additional game logic:
		if circularspritesoverlap(self.cursor, self.target):
			# hit. 
			# todo: increment counter of targets hit
			self.target.pickedup()
			# reposition target
			self.target.rect.left = self.rnd.randint(0, self.screenarea.width - self.target.diameter)
			self.target.rect.top = self.rnd.randint(0, self.screenarea.height - self.target.diameter)
		for asteroid in self.asteroids:
			if circularspritesoverlap(self.cursor, asteroid):
				# todo: find a cleaner way to have the shield powerup do this work:
				if not (self.powerup != None and self.powerup.__class__ == ShieldPowerup and self.powerup.active):
					self.sound_death.play()
					print 'dead', self.cursor.rect.left, self.cursor.rect.top
					self.screenstack.append(GameOverOverlayScreen(self.screen, self.screenstack))
					break
		# powerups?
		if self.powerup != None \
			and circularspritesoverlap(self.cursor, self.powerup) \
			and not self.powerup.active \
			and not self.powerup.used:
			print 'hit powerup', self.cursor.rect.left, self.cursor.rect.top, self.powerup
			# TODO: decide where and when to spawn next powerup
			# how should powerup behavior be implemented?
			self.powerup.activate(self.cursor, self.asteroids)

	def draw(self):
		self.screen.blit(self.background, (0, 0))
		self.mostsprites.draw(self.screen)
		self.powerupsprites.draw(self.screen)


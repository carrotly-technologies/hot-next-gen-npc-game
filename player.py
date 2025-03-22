import pygame
from pygame.math import Vector2 

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, frames, sprites, collision_sprites):
		super().__init__(sprites)

		self.collision_sprites = collision_sprites
		self.pos = pos
		self.frame_index, self.frames = 0, frames
		self.direction = Vector2()
		self.speed = 250

		self.image = self.frames[self.get_state()][self.frame_index]
		self.rect = self.image.get_frect(center = pos)
		self.hitbox = self.rect.inflate(-self.rect.width / 2, -60)

		self.frame_index = 0
		self.frames = frames
		self.image = self.frames[self.get_state()][self.frame_index]

		self.rect = self.image.get_frect(center = pos)
		self.blocked = False

	def input(self):
		keys = pygame.key.get_pressed()
		input_vector = Vector2()
		if keys[pygame.K_UP]:
			input_vector.y -= 1
		if keys[pygame.K_DOWN]:
			input_vector.y += 1
		if keys[pygame.K_LEFT]:
			input_vector.x -= 1
		if keys[pygame.K_RIGHT]:
			input_vector.x += 1
		self.direction = input_vector.normalize() if input_vector else input_vector

	def collisions(self, axis):
		for sprite in self.collision_sprites:
			if sprite.hitbox.colliderect(self.hitbox):
				if axis == 'horizontal':
					if self.direction.x > 0:
						self.hitbox.right = sprite.hitbox.left
					if self.direction.x < 0:
						self.hitbox.left = sprite.hitbox.right
					self.rect.centerx = self.hitbox.centerx
				else:
					if self.direction.y > 0:
						self.hitbox.bottom = sprite.hitbox.top
					if self.direction.y < 0:
						self.hitbox.top = sprite.hitbox.bottom
					self.rect.centery = self.hitbox.centery

	def move(self, dt):
		self.rect.centerx += self.direction.x * self.speed * dt
		self.hitbox.centerx = self.rect.centerx
		self.collisions('horizontal')

		self.rect.centery += self.direction.y * self.speed * dt
		self.hitbox.centery = self.rect.centery
		self.collisions('vertical')

	def animate(self, dt):
		self.frame_index += 6 * dt
		self.image = self.frames[self.get_state()][int(self.frame_index % len(self.frames[self.get_state()]))]

	def update(self, dt):
		self.input()

		if not self.blocked:
			self.move(dt)
			self.animate(dt)

	def get_state(self):
		moving = bool(self.direction)
		if moving:
			if self.direction.x != 0:
				return 'right' if self.direction.x > 0 else 'left'
			if self.direction.y != 0:
				return 'down' if self.direction.y > 0 else 'up' 
		return "down_idle"
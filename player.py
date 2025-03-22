import pygame
from pygame.math import Vector2 

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, frames, sprites):
		super().__init__(sprites)
		
		self.pos = pos
		self.frames = frames
		self.direction = Vector2()
		self.speed = 250

		self.frame_index = 0
		self.frames = frames
		self.image = self.frames[self.get_state()][self.frame_index]

		self.rect = self.image.get_frect(center = pos)

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

	def move(self, dt):
		self.rect.centerx += self.direction.x * self.speed * dt
		self.rect.centery += self.direction.y * self.speed * dt

	def animate(self, dt):
		self.frame_index += 6 * dt
		self.image = self.frames[self.get_state()][int(self.frame_index % len(self.frames[self.get_state()]))]

	def update(self, dt):
		self.input()
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
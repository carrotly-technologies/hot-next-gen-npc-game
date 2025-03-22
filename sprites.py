import pygame
from pygame.math import Vector2 
from settings import * 

class Sprites(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.offset = Vector2()

	def draw(self, player):
		self.offset.x = -(player.rect.centerx - WIDTH / 2)
		self.offset.y = -(player.rect.centery - HEIGHT / 2)

		sprites = [sprite for sprite in self]

		for sprite in sprites:
			self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)


class Sprite(pygame.sprite.Sprite):
	def __init__(self, pos, surf, groups, z = WORLD_LAYERS['main']):
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_frect(topleft = pos)
		self.z = z
		self.y_sort = self.rect.centery
		self.hitbox = self.rect.copy()

class BorderSprite(Sprite):
	def __init__(self, pos, surf, groups):
		super().__init__(pos, surf, groups)
		self.hitbox = self.rect.copy()

class TransitionSprite(Sprite):
	def __init__(self, pos, size, target, groups):
		surf = pygame.Surface(size)
		super().__init__(pos, surf, groups)
		self.target = target

class CollidableSprite(Sprite):
	def __init__(self, pos, surf, groups):
		super().__init__(pos, surf, groups)
		self.hitbox = self.rect.inflate(0, -self.rect.height * 0.6)

class AnimatedSprite(Sprite):
	def __init__(self, pos, frames, groups, z = WORLD_LAYERS['main']):
		self.frame_index, self.frames = 0, frames
		super().__init__(pos, frames[self.frame_index], groups, z)

	def animate(self, dt):
		self.frame_index += ANIMATION_SPEED * dt
		self.image = self.frames[int(self.frame_index % len(self.frames))]

	def update(self, dt):
		self.animate(dt)

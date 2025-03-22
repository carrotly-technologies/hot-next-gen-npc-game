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


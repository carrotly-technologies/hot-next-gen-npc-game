import pygame

class Npc(pygame.sprite.Sprite):
	def __init__(self, pos, frames, sprites):
		super().__init__(sprites)
		
		self.pos = pos
		self.frames = frames

		self.frames = frames
		self.image = self.frames["down"][0]

		self.rect = self.image.get_frect(center = pos)
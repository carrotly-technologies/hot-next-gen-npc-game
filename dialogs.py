import pygame
from settings import *
from pygame.math import Vector2

class Dialog:
	def __init__(self, player, npc, sprites, font): 
		# self.current_dialog = DialogSprite(self.dialog[self.dialog_index], self.character, self.all_sprites, self.font)
		self.player = player
		self.npc = npc
		self.sprites = sprites
		self.font = font

		self.sprite = DialogSprite('Hello World', self.npc, self.sprites, self.font)
    
	def input(self):
		keys = pygame.key.get_just_pressed()
		if keys[pygame.K_SPACE]:
			self.sprite.kill()
			self.sprite = DialogSprite('Goodbye World', self.npc, self.sprites, self.font)

	def update(self):
		self.input()


class DialogSprite(pygame.sprite.Sprite):
	def __init__(self, message, npc, sprites, font):
		super().__init__(sprites)
		
		text = font.render(message, False, '#000000')
		padding = 5
		width = max(30, text.get_width() + padding * 2)
		height = text.get_height() + padding * 2

		surf = pygame.Surface((width, height), pygame.SRCALPHA)
		surf.fill((0,0,0,0))
		pygame.draw.rect(surf, '#ffffff', surf.get_frect(topleft = (0,0)),0, 4)
		surf.blit(text, text.get_frect(center = (width / 2, height / 2)))

		self.image = surf
		self.rect = self.image.get_frect(midbottom = npc.rect.midtop + Vector2(0,-10))
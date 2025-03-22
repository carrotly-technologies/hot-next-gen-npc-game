#!/usr/bin/env python
"""pygame.examples.moveit

This is the full and final example from the Pygame Tutorial,
"How Do I Make It Move". It creates 10 objects and animates
them on the screen.

It also has a separate player character that can be controlled with arrow keys.

Note it's a bit scant on error checking, but it's easy to read. :]
Fortunately, this is python, and we needn't wrestle with a pile of
error codes.
"""

import os
import pygame
from pygame.math import Vector2
from player import Player
from sprites import Sprites
from dialogs import Dialog
from npcs import Npc
from loaders import load_all_characters
from settings import *
from os.path import join

main_dir = os.path.split(os.path.abspath(__file__))[0]

class Game:
	def __init__(self):
		pygame.init()
		pygame.display.set_caption('Hack of Tomorrow')
		self.display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
		self.clock = pygame.time.Clock()

		self.transition_target = None
		self.tint_surf = pygame.Surface((WIDTH, HEIGHT))
		self.tint_mode = 'untint'
		self.tint_progress = 0
		self.tint_direction = -1
		self.tint_speed = 600

		self.sprites = Sprites()
		self.dialog = None

		self.load_assets()
		self.player = Player(Vector2(0, 0), self.frames['characters']['fire_boss'], self.sprites)
		self.npc = Npc(Vector2(0, 100), self.frames['characters']['hat_girl'], self.sprites) 

	def load_assets(self):
		self.frames = { 'characters': load_all_characters('data', 'graphics', 'characters') }

		self.fonts = { 'dialog': pygame.font.Font(join('data', 'fonts', 'PixeloidSans.ttf'), 30) }


	def tint_screen(self, dt):
		if self.tint_mode == 'untint':
			self.tint_progress -= self.tint_speed * dt

		if self.tint_mode == 'tint':
			self.tint_progress += self.tint_speed * dt
			if self.tint_progress >= 255:
				if self.transition_target == 'level':
					self.battle = None
				else:
					self.setup(self.tmx_maps[self.transition_target[0]], self.transition_target[1])
				self.tint_mode = 'untint'
				self.transition_target = None

		self.tint_progress = max(0, min(self.tint_progress, 255))
		self.tint_surf.set_alpha(self.tint_progress)
		self.display_surface.blit(self.tint_surf, (0,0))

	def run(self):
		while True:
			dt = self.clock.tick() / 1000
			self.display_surface.fill('black')

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()

			keys = pygame.key.get_pressed()
			if keys[pygame.K_w]:
				self.dialog = Dialog(self.player, npc, self.sprites, self.fonts['dialog'])
				self.player.blocked = True

			self.sprites.update(dt)
			self.sprites.draw(self.player)

			if self.dialog: self.dialog.update()

			self.tint_screen(dt)
			pygame.display.update()
        
def load_image(name):
    path = os.path.join(main_dir, "data", name)
    return pygame.image.load(path).convert()

if __name__ == "__main__":
    game = Game()
    game.run()
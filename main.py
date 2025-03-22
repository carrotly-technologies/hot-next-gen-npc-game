#!/usr/bin/env python

import os
from os.path import join

import pygame

from loaders import load_all_characters, tmx_importer
from player import Player
from dialogs import Dialog
from npcs import Npc
from loaders import load_all_characters
from settings import *
from os.path import join
from settings import *
from sprites import Sprites, Sprite, CollidableSprite, BorderSprite, AnimatedSprite
from pygame.math import Vector2

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

		self.collision_sprites = pygame.sprite.Group()
		self.character_sprites = pygame.sprite.Group()
		self.transition_sprites = pygame.sprite.Group()

		self.sprites = Sprites()
		self.dialog = None

		self.load_assets()
		self.setup(self.tmx_maps['world_map'], 'house')

		# self.player = Player(Vector2(0, 0), self.frames['characters']['fire_boss'], self.sprites, self.collision_sprites)
		self.npc = Npc(Vector2(0, 100), self.frames['characters']['hat_girl'], self.sprites) 


	def load_assets(self):
		self.tmx_maps = tmx_importer('data', 'maps')

		self.frames = { 'characters': load_all_characters('data', 'graphics', 'characters') }

		self.fonts = {
			'dialog': pygame.font.Font(join('data', 'graphics', 'fonts', 'PixeloidSans.ttf'), 30),
			'regular': pygame.font.Font(join('data', 'graphics', 'fonts', 'PixeloidSans.ttf'), 18),
			'small': pygame.font.Font(join('data', 'graphics', 'fonts', 'PixeloidSans.ttf'), 14),
			'bold': pygame.font.Font(join('data', 'graphics', 'fonts', 'dogicapixelbold.otf'), 20),
		}


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

	def setup(self, tmx_map, player_start_pos):
		# clear the map
		for group in (self.sprites, self.collision_sprites, self.transition_sprites, self.character_sprites):
			group.empty()

		# terrain
		for layer in ['Terrain']:
			for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
				Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.sprites, WORLD_LAYERS['bg'])

		# objects
		for obj in tmx_map.get_layer_by_name('Objects'):
			if obj.name == 'top':
				Sprite((obj.x, obj.y), obj.image, self.sprites, WORLD_LAYERS['top'])
			else:
				CollidableSprite((obj.x, obj.y), obj.image, (self.sprites, self.collision_sprites))

		# transition objects
		# for obj in tmx_map.get_layer_by_name('Transition'):
		# 	TransitionSprite((obj.x, obj.y), (obj.width, obj.height), (obj.properties['target'], obj.properties['pos']),
		# 					 self.transition_sprites)

		# collision objects
		for obj in tmx_map.get_layer_by_name('Collisions'):
			BorderSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

		# entities
		for obj in tmx_map.get_layer_by_name('Entities'):
			if obj.name == 'Player':
				if obj.properties['pos'] == player_start_pos:
					self.player = Player((obj.x, obj.y), self.frames['characters']['fire_boss'], self.sprites, self.collision_sprites)

	def run(self):
		while True:
			dt = self.clock.tick() / 1000
			self.display_surface.fill('pink')

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()

			# Temporary dialog trigger, it should be moved to better place
			# First we should check if NPC is in range of player
			# Second we should check if player is pressing the right key
			keys = pygame.key.get_pressed()
			if not self.dialog and keys[pygame.K_w]:
				self.dialog = Dialog(self.player, self.npc, self.sprites, self.fonts['dialog'])
				self.player.blocked = True

			if self.dialog and keys[pygame.K_ESCAPE]:
				self.dialog.sprite.kill()
				self.dialog = None
				self.player.blocked = False

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
#!/usr/bin/env python

import os
from os.path import join

import pygame
import xml.etree.ElementTree as ET

from loaders import load_all_characters, tmx_importer
from player import Player
from dialogs import Dialog
from npcs import Npc
from loaders import load_all_characters
from settings import *
from os.path import join
from settings import *
from sprites import Sprites, Sprite, CollidableSprite, BorderSprite, AnimatedSprite, TransitionSprite
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
		self.setup(self.tmx_maps['world_map'], 'init')

		self.remixed_map_data = [
			[17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17],
			[17, 29, 30, 17, 17, 17, 17, 17, 17, 17, 17, 17, 39, 40, 17],
			[17, 17, 17, 9, 4, 4, 9, 4, 9, 4, 9, 9, 17, 17, 17],
			[17, 17, 17, 4, 9, 4, 9, 4, 9, 4, 9, 4, 17, 17, 17],
			[17, 17, 17, 9, 4, 9, 4, 4, 4, 9, 4, 9, 17, 17, 17],
			[17, 17, 17, 4, 9, 4, 9, 4, 9, 4, 9, 4, 17, 17, 17],
			[17, 17, 17, 9, 4, 9, 4, 9, 4, 9, 4, 9, 17, 17, 17],
			[17, 17, 17, 4, 4, 4, 4, 4, 4, 4, 4, 4, 17, 17, 17],
			[17, 17, 17, 9, 4, 9, 4, 9, 4, 9, 4, 9, 17, 17, 17],
			[17, 17, 17, 4, 9, 4, 9, 4, 9, 4, 9, 4, 17, 17, 17],
			[17, 17, 17, 9, 4, 9, 4, 9, 4, 9, 4, 9, 17, 17, 17],
			[17, 17, 17, 4, 9, 4, 9, 4, 9, 4, 9, 4, 17, 17, 17],
			[17, 24, 25, 17, 17, 17, 17, 17, 17, 17, 17, 17, 34, 35, 17],
			[17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17],
			[17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17]
		]

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

	def save_patched_map(self, base_map_path, output_path):
		# Load the base map from disk
		tree = ET.parse(base_map_path)
		root = tree.getroot()

		# Find the terrain layer
		for layer in root.findall("layer"):
			if layer.attrib.get("name") == "Terrain":
				data = layer.find("data")
				if data is not None:
					# Convert remixed data to CSV string
					csv_string = "\n" + ",\n".join(
						",".join(str(gid) for gid in row) for row in self.remixed_map_data
					)
					data.text = csv_string
					break

		# Save new patched file
		tree.write(output_path)

	def setup(self, tmx_map, player_start_pos):
		# clear the map
		for group in (self.sprites, self.collision_sprites, self.transition_sprites, self.character_sprites):
			group.empty()

		if player_start_pos == "house-in":
			base_path = join('data', 'maps', 'room_map.tmx')
			output_path = join('data', 'maps', 'patched_room_map.tmx')
			self.save_patched_map(base_path, output_path)
			tmx_map = tmx_importer('data', 'maps')['patched_room_map']

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
		for obj in tmx_map.get_layer_by_name('Transition'):
			TransitionSprite((obj.x, obj.y), (obj.width, obj.height), (obj.properties['target'], obj.properties['pos']),
							 self.transition_sprites)

		# collision objects
		for obj in tmx_map.get_layer_by_name('Collisions'):
			BorderSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

		# entities
		for obj in tmx_map.get_layer_by_name('Entities'):
			if obj.name == 'Player':
				if obj.properties['pos'] == player_start_pos:
					self.player = Player((obj.x, obj.y), self.frames['characters']['fire_boss'], self.sprites, self.collision_sprites)
			elif obj.name == 'NPC1':
				dialog = [
					{
						'message': 'Hello! How can I help you?',
						'options': [
							{ 'text': 'Nevermind, goodbye!', 'finish': True },
							{ 'text': 'How are you?', 'next': 1 },
							{ 'text': 'What is your name?', 'next': 2 }
						]
					},
					{
						'message': 'I am quite busy these days, but I am doing well. Unfortunately I cannot chat for now. Goodbye!',
						'finish': True
					},
					{
						'message': 'My name is John. What is your name?',
						'options': [
							{ 'text': 'I am Bob', 'next': 3 },
							{ 'text': 'I am Alice', 'next': 4 },
						]
					},
					{
						'message': 'Nice to meet you Bob! Goodbye!',
						'finish': True
					},
					{
						'message': 'Nice to meet you Alice! Goodbye!',
						'finish': True
					}
				]
				self.npc = Npc((obj.x, obj.y), self.frames['characters']['hat_girl'], self.sprites, dialog)

	def on_dialog_end(self):
		self.dialog = None
		self.player.blocked = False

	def transition_check(self):
		sprites = [sprite for sprite in self.transition_sprites if sprite.rect.colliderect(self.player.hitbox)]
		if sprites:
			# should block player but you know
			self.transition_target = sprites[0].target
			self.tint_mode = 'tint'

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
				self.dialog = Dialog(self.player, self.npc, self.sprites, self.fonts['dialog'], self.on_dialog_end)
				self.player.blocked = True


			self.transition_check()
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
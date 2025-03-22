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
				# Temporarlily hardcoded dialog, but it should be managed dynamically by AI agent
				dialog = [
					{
						"message": "Greetings, traveler! What brings you to my humble stall today?",
						"options": [
							{
								"text": "I heard you have a rare artifact for sale.",
								"next": 1,
								"finish": None
							},
							{
								"text": "Just browsing, thanks.",
								"next": 2,
								"finish": None
							}
						],
						"finish": None
					},
					{
						"message": "Ah, yes. I do have something special, but I must know if you can really appreciate its value.",
						"options": [
							{
								"text": "Tell me more about it.",
								"next": 3,
								"finish": None
							},
							{
								"text": "How much are you asking for it?",
								"next": 4,
								"finish": None
							}
						],
						"finish": None
					},
					{
						"message": "Of course, take your time. Perhaps you'll find something that catches your eye.",
						"options": [
							{
								"text": "What's this artifact you have?",
								"next": 1,
								"finish": None
							},
							{
								"text": "Thanks, I'll come back later.",
								"next": 5,
								"finish": True
							}
						],
						"finish": None
					},
					{
						"message": "This artifact is said to be from the Desert of Whispers, with a tale shrouded in mystery and perhaps magic.",
						"options": [
							{
								"text": "What do you mean by magic?",
								"next": 6,
								"finish": None
							},
							{
								"text": "Sounds intriguing. How much?",
								"next": 4,
								"finish": None
							}
						],
						"finish": None
					},
					{
						"message": "The price starts at 500 gold, but I'm open to negotiation if you're truly interested.",
						"options": [
							{
								"text": "That's steep. Can you go lower?",
								"next": 7,
								"finish": None
							},
							{
								"text": "I'll take it for 500 gold.",
								"next": 8,
								"finish": True
							}
						],
						"finish": None
					},
					{
						"message": "Safe travels, then! I'll be here when you return.",
						"options": None,
						"finish": True
					},
					{
						"message": "Magic is a rare commodity these days. The artifact may possess unusual properties.",
						"options": [
							{
								"text": "Can you prove it has magic?",
								"next": 9,
								"finish": None
							},
							{
								"text": "Alright, how much is it again?",
								"next": 4,
								"finish": None
							}
						],
						"finish": None
					},
					{
						"message": "If you can offer 350 gold, it might just be yours.",
						"options": [
							{
								"text": "Deal at 350 gold.",
								"next": 8,
								"finish": True
							},
							{
								"text": "I need to think about it.",
								"next": 5,
								"finish": True
							}
						],
						"finish": None
					},
					{
						"message": "Pleasure doing business with you! May the artifact serve you well.",
						"options": None,
						"finish": True
					},
					{
						"message": "I'm afraid you'll have to take me at my word—such things aren't easily demonstrated in public streets.",
						"options": [
							{
								"text": "Alright, I'll buy it for 350 gold.",
								"next": 8,
								"finish": True
							},
							{
								"text": "I'll pass for now.",
								"next": 5,
								"finish": True
							}
						],
						"finish": None
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
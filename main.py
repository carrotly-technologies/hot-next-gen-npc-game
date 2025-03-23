#!/usr/bin/env python

import asyncio
import os
import xml.etree.ElementTree as ET
from os.path import join

import pygame
from pygame.constants import SCALED
from pygame.math import Vector2
from pygame.event import get as get_events
from pygame.display import set_mode, flip

from dialogs import Dialog
from loaders import load_all_characters, tmx_importer
from mocks import *
from npcs import Npc
from player import Player
from settings import *
from sprites import Sprites, Sprite, CollidableSprite, BorderSprite, TransitionSprite

main_dir = os.path.split(os.path.abspath(__file__))[0]


class Game:
	def __init__(self):
		pygame.init()
		pygame.display.set_caption('Hack of Tomorrow')
		self.display_surface = set_mode((WIDTH, HEIGHT), flags=SCALED, vsync=1)

		self.transition_target = None
		self.tint_surf = pygame.Surface((WIDTH, HEIGHT))
		self.tint_mode = 'untint'
		self.tint_progress = 0
		self.tint_speed = 600

		self.collision_sprites = pygame.sprite.Group()
		self.character_sprites = pygame.sprite.Group()
		self.transition_sprites = pygame.sprite.Group()

		self.sprites = Sprites()
		self.dialog = None

		self.load_assets()
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
		self.setup(self.tmx_maps['world_map'], 'init')

	def load_assets(self):
		self.tmx_maps = tmx_importer('data', 'maps')
		self.frames = {'characters': load_all_characters('data', 'graphics', 'characters')}
		self.fonts = {
			'dialog': pygame.font.Font(join('data', 'graphics', 'fonts', 'PixeloidSans.ttf'), 30),
			'regular': pygame.font.Font(join('data', 'graphics', 'fonts', 'PixeloidSans.ttf'), 18),
			'small': pygame.font.Font(join('data', 'graphics', 'fonts', 'PixeloidSans.ttf'), 14),
			'bold': pygame.font.Font(join('data', 'graphics', 'fonts', 'dogicapixelbold.otf'), 20),
		}

	def save_patched_map(self, base_map_path, output_path):
		tree = ET.parse(base_map_path)
		root = tree.getroot()

		for layer in root.findall("layer"):
			if layer.attrib.get("name") == "Terrain":
				data = layer.find("data")
				if data is not None:
					csv_string = "\n" + ",\n".join(
						",".join(str(gid) for gid in row) for row in self.remixed_map_data
					)
					data.text = csv_string
					break

		tree.write(output_path)

	async def delayed_patch_and_reload(self, base_path, output_path):
		await asyncio.sleep(1)
		self.save_patched_map(base_path, output_path)
		tmx_map = tmx_importer('data', 'maps')['patched_room_map']
		self.setup(tmx_map, 'house-in', skipCheck=True)

	def setup(self, tmx_map, player_start_pos, skipCheck = False):
		for group in (self.sprites, self.collision_sprites, self.transition_sprites, self.character_sprites):
			group.empty()

		if player_start_pos == "house-in" and not skipCheck:
			base_path = join('data', 'maps', 'room_map.tmx')
			output_path = join('data', 'maps', 'patched_room_map.tmx')
			asyncio.create_task(self.delayed_patch_and_reload(base_path, output_path))
			return

		for layer in ['Terrain']:
			for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
				Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.sprites, WORLD_LAYERS['bg'])

		for obj in tmx_map.get_layer_by_name('Objects'):
			if obj.name == 'top':
				Sprite((obj.x, obj.y), obj.image, self.sprites, WORLD_LAYERS['top'])
			else:
				CollidableSprite((obj.x, obj.y), obj.image, (self.sprites, self.collision_sprites))

		for obj in tmx_map.get_layer_by_name('Transition'):
			TransitionSprite((obj.x, obj.y), (obj.width, obj.height), (obj.properties['target'], obj.properties['pos']),
							 self.transition_sprites)

		for obj in tmx_map.get_layer_by_name('Collisions'):
			BorderSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

		for obj in tmx_map.get_layer_by_name('Entities'):
			if obj.name == 'Player' and obj.properties['pos'] == player_start_pos:
				self.player = Player((obj.x, obj.y), self.frames['characters']['fire_boss'],
									 self.sprites, self.collision_sprites)
			elif obj.name == 'NPC1':
				dialog = DIALOGUE_3
				self.npc = Npc((obj.x, obj.y), self.frames['characters']['hat_girl'], self.sprites, dialog)

	def on_dialog_end(self):
		self.dialog = None
		self.player.blocked = False

	def transition_check(self):
		sprites = [sprite for sprite in self.transition_sprites if sprite.rect.colliderect(self.player.hitbox)]
		if sprites:
			self.transition_target = sprites[0].target
			self.tint_mode = 'tint'

	def tint_screen(self, dt):
		if self.tint_mode == 'untint':
			self.tint_progress -= self.tint_speed * dt
		elif self.tint_mode == 'tint':
			self.tint_progress += self.tint_speed * dt
			if self.tint_progress >= 255:
				if self.transition_target:
					self.setup(self.tmx_maps[self.transition_target[0]], self.transition_target[1])
				self.tint_mode = 'untint'
				self.transition_target = None

		self.tint_progress = max(0, min(self.tint_progress, 255))
		self.tint_surf.set_alpha(self.tint_progress)
		self.display_surface.blit(self.tint_surf, (0, 0))

	async def run(self, event_queue: asyncio.Queue, framerate=60):
		frame_duration = 1.0 / framerate
		loop = asyncio.get_event_loop()

		while True:
			start = loop.time()

			# Handle all pending events from the queue
			while not event_queue.empty():
				event = await event_queue.get()
				if event.type == pygame.QUIT:
					pygame.quit()
					raise SystemExit

				# Example input handling
				if not self.dialog and event.type == pygame.KEYDOWN and event.key == pygame.K_w:
					self.dialog = Dialog(self.player, self.npc, self.sprites, self.fonts['dialog'], self.on_dialog_end)
					self.player.blocked = True

			# Update & Draw
			dt = frame_duration
			self.display_surface.fill('black')

			self.transition_check()
			self.sprites.update(dt)
			self.sprites.draw(self.player)

			if self.dialog:
				self.dialog.update()

			self.tint_screen(dt)
			await loop.run_in_executor(None, flip)

			# Frame limit
			elapsed = loop.time() - start
			sleep_time = max(0, frame_duration - elapsed)
			await asyncio.sleep(sleep_time)


def load_image(name):
	path = os.path.join(main_dir, "data", name)
	return pygame.image.load(path).convert()

async def pygame_event_loop(event_queue: asyncio.Queue):
	while True:
		await asyncio.sleep(0)
		event = pygame.event.poll()
		if event.type != pygame.NOEVENT:
			await event_queue.put(event)



async def main():
	event_queue = asyncio.Queue()
	game = Game()

	# Start both the event loop and game loop
	await asyncio.gather(
		pygame_event_loop(event_queue),
		game.run(event_queue)
	)

if __name__ == "__main__":
	asyncio.run(main())

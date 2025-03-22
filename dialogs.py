import pygame
from settings import *
from pygame.math import Vector2

class Dialog:
	def __init__(self, player, npc, sprites, font, on_end):
		self.player = player
		self.npc = npc
		self.sprites = sprites
		self.font = font

		self.dialog = npc.dialog
		self.on_end = on_end
		self.timer = None 

		self.npc_sprite = DialogNpc(self.dialog[0]['message'], self.npc, self.sprites, self.font)
		
		if 'options' in self.dialog[0] and self.dialog[0]['options']:
			self.player_sprite = DialogOptionsController(self.dialog[0]['options'], self.player, self.sprites, self.font)
		else:
			self.player_sprite = None
			self.timer = pygame.time.get_ticks() + 2000

	def dispose(self):
		self.npc_sprite.kill()
		if self.player_sprite: self.player_sprite.kill()

	def input(self):
		keys = pygame.key.get_just_pressed()
		if keys[pygame.K_RETURN]:
			option = self.player_sprite.get_selected_option()
			if 'finish' in option and option['finish']:
				self.dispose()
				self.on_end()
			else:
				self.dispose()
				dialog = self.dialog[option['next']]

				if 'finish' in dialog and dialog['finish']:
					self.npc_sprite = DialogNpc(dialog['message'], self.npc, self.sprites, self.font)
					self.timer = pygame.time.get_ticks() + 2000
				else:
					self.player_sprite = DialogOptionsController(dialog['options'], self.player, self.sprites, self.font)
					self.npc_sprite = DialogNpc(dialog['message'], self.npc, self.sprites, self.font)

	def update(self):
		self.input()
		if self.player_sprite:
			self.player_sprite.input()

		if self.timer and pygame.time.get_ticks() >= self.timer:
			self.dispose()
			self.on_end()
			self.timer = None  

class DialogNpc(pygame.sprite.Sprite):
	def __init__(self, message, npc, sprites, font):
		super().__init__(sprites)
		
		max_width = 500  # Maximum width in pixels for the dialog frame
		padding = 5
		
		# Split message into words
		words = message.split(' ')
		lines = []
		current_line = words[0]
		
		# Create lines that fit within max_width
		for word in words[1:]:
			test_line = current_line + ' ' + word
			test_width = font.size(test_line)[0]
			
			if test_width + padding * 2 <= max_width:
				current_line = test_line
			else:
				lines.append(current_line)
				current_line = word
		
		lines.append(current_line)  # Add the last line
		
		# Render each line of text
		rendered_lines = [font.render(line, False, '#000000') for line in lines]
		
		# Calculate dialog dimensions
		line_height = font.get_height()
		width = max(30, min(max_width, max(line.get_width() for line in rendered_lines) + padding * 2))
		height = len(lines) * line_height + padding * 2
		
		# Create the dialog surface
		surf = pygame.Surface((width, height), pygame.SRCALPHA)
		surf.fill((0, 0, 0, 0))
		pygame.draw.rect(surf, '#ffffff', surf.get_frect(topleft=(0, 0)), 0, 4)
		
		# Blit each line onto the dialog surface
		for i, line in enumerate(rendered_lines):
			y_pos = padding + i * line_height
			surf.blit(line, line.get_frect(midtop=(width / 2, y_pos)))
		
		self.image = surf
		self.rect = self.image.get_frect(midbottom=npc.rect.midtop + Vector2(0, -10))

class DialogOption(pygame.sprite.Sprite):
	def __init__(self, option, position, font, sprites, is_active=False):
		super().__init__(sprites)
		self.text = option['text']
		self.font = font
		self.is_active = is_active
		self.position = position
		self.sprites = sprites
		self.update_image()
		
	def update_image(self):
		text_color = '#00FF00' if self.is_active else '#000000'
		text_surf = self.font.render(self.text, False, text_color)

		padding = 5
		
		screen_width, screen_height = pygame.display.get_surface().get_size()
		width = screen_width - 40
		height = text_surf.get_height() + padding * 2
		surf = pygame.Surface((width, height), pygame.SRCALPHA)
		surf.fill((0, 0, 0, 0))
		
		pygame.draw.rect(surf, '#ffffff', surf.get_rect(), 0, 4)
		surf.blit(text_surf, text_surf.get_rect(midtop=(text_surf.get_width() / 2 + 10, padding)))
		
		self.image = surf
		self.rect = self.image.get_rect(center=self.position)
		
	def set_active(self, active):
		if self.is_active != active:
			self.is_active = active
			self.update_image()


class DialogOptionsController(pygame.sprite.Sprite):
	def __init__(self, options, player, sprites, font):
		super().__init__()
		
		self.options = options
		self.option_sprites = []
		self.current_option = 0
		self.sprites = sprites
		self.font = font

		self.key_up_pressed = False
		self.key_down_pressed = False
		self.key_select_pressed = False
		
		_, screen_height = pygame.display.get_surface().get_size()
		padding = 5
		option_height = font.get_linesize() + padding * 2
		total_height = option_height * len(options)
		
		start_y = player.rect.centery + screen_height / 2 - total_height
		x_position = player.rect.centerx
		
		for i, option in enumerate(options):
			y_position = start_y + i * option_height
			is_active = (i == 0)  
			
			option = DialogOption(
				option, 
				(x_position, y_position), 
				font, 
				sprites, 
				is_active
			)
			self.option_sprites.append(option)
	
	def input(self):
		keys = pygame.key.get_pressed()
		
		if keys[pygame.K_UP]:
			if not self.key_up_pressed:
				self.key_up_pressed = True
				old_option = self.current_option
				self.current_option = max(0, self.current_option - 1)
				
				if old_option != self.current_option:
					self.option_sprites[old_option].set_active(False)
					self.option_sprites[self.current_option].set_active(True)
		else:
			self.key_up_pressed = False
			
		if keys[pygame.K_DOWN]:
			if not self.key_down_pressed:
				self.key_down_pressed = True
				old_option = self.current_option
				self.current_option = min(len(self.option_sprites) - 1, self.current_option + 1)

				if old_option != self.current_option:
					self.option_sprites[old_option].set_active(False)
					self.option_sprites[self.current_option].set_active(True)
		else:
			self.key_down_pressed = False
		
		if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
			if not self.key_select_pressed:
				self.key_select_pressed = True
				return self.current_option
		else:
			self.key_select_pressed = False
		
	def get_selected_option(self):
		return self.options[self.current_option]
	
	def kill(self):
		for option in self.option_sprites:
			option.kill()
		super().kill()
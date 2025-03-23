#!/usr/bin/env python

import os
import xml.etree.ElementTree as ET
from os.path import join

from pygame.event import get as get_events

from dialogs import Dialog
from loaders import load_all_characters, tmx_importer
from mocks import *
from npc_engine import call_npc_engine_api, call_npc_engine_api_area
from npcs import *
from player import Player
from settings import *
from sprites import Sprites, Sprite, CollidableSprite, BorderSprite, TransitionSprite

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
        self.dialogs = []

        self.collision_sprites = pygame.sprite.Group()
        self.character_sprites = pygame.sprite.Group()
        self.transition_sprites = pygame.sprite.Group()

        self.sprites = Sprites()
        self.dialog = None

        self.load_assets()
        self.remixed_map_data = [
            [
                134,
                134,
                134,
                134,
                134,
                134,
                134,
                134,
                134,
                134,
                134,
                134,
                134,
                134,
                134
            ],
            [
                134,
                17,
                17,
                17,
                17,
                17,
                17,
                17,
                17,
                17,
                17,
                17,
                17,
                17,
                134
            ],
            [
                134,
                17,
                97,
                97,
                97,
                97,
                97,
                97,
                97,
                97,
                97,
                97,
                97,
                17,
                134
            ],
            [
                134,
                17,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                17,
                134
            ],
            [
                134,
                17,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                17,
                134
            ],
            [
                134,
                17,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                17,
                134
            ],
            [
                134,
                17,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                17,
                134
            ],
            [
                134,
                17,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                17,
                134
            ],
            [
                134,
                17,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                17,
                134
            ],
            [
                134,
                17,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                17,
                134
            ],
            [
                134,
                17,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                17,
                134
            ],
            [
                134,
                17,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                9,
                17,
                134
            ],
            [
                134,
                17,
                97,
                97,
                97,
                97,
                97,
                97,
                97,
                97,
                97,
                97,
                97,
                17,
                134
            ],
            [
                134,
                17,
                17,
                17,
                17,
                17,
                17,
                17,
                17,
                17,
                17,
                17,
                17,
                17,
                134
            ],
            [
                134,
                134,
                134,
                134,
                134,
                134,
                134,
                134,
                134,
                134,
                134,
                134,
                134,
                134,
                134
            ]
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

    def save_patched_map(self, base_map_path, output_path, ret: str):
        tree = ET.parse(base_map_path)
        root = tree.getroot()

        for layer in root.findall("layer"):
            if layer.attrib.get("name") == "Terrain":
                data = layer.find("data")
                if data is not None:
                    data.text = "\n" + ret + "\n"
                    break

        tree.write(output_path)

    def setup(self, tmx_map, player_start_pos, skipCheck=False):
        for group in (self.sprites, self.collision_sprites, self.transition_sprites, self.character_sprites):
            group.empty()

        if player_start_pos == "house-in":
            messages = []
            if len(self.dialogs) > 0:
                for a in self.dialogs[0]:
                    messages.append(a['message'])

            ret = call_npc_engine_api_area(messages)

            base_path = join('data', 'maps', 'room_map.tmx')
            output_path = join('data', 'maps', 'patched_room_map.tmx')
            self.save_patched_map(base_path, output_path, ret)
            tmx_map = tmx_importer('data', 'maps')['patched_room_map']

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

        self.npcs = []

        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player' and obj.properties['pos'] == player_start_pos:
                self.player = Player((obj.x, obj.y), self.frames['characters']['fire_boss'],
                                     self.sprites, self.collision_sprites)
            elif obj.name == 'NPC1':
                self.npcs.append(
                    Npc((obj.x, obj.y), self.frames['characters']['hat_girl'], self.sprites, [], SARAH_NPC))
            elif obj.name == 'NPC2':
                self.npcs.append(Npc((obj.x, obj.y), self.frames['characters']['blond'], self.sprites, [], ANNA_NPC))
            elif obj.name == 'NPC3':
                self.npcs.append(
                    Npc((obj.x, obj.y), self.frames['characters']['young_guy'], self.sprites, [], JOHN_NPC))
            elif obj.name == 'NPC4':
                self.npcs.append(
                    Npc((obj.x, obj.y), self.frames['characters']['water_boss'], self.sprites, [], CAROLINE_NPC))

    def on_dialog_end(self):
        self.dialog = None
        self.player.blocked = False

    def transition_check(self):
        sprites = [sprite for sprite in self.transition_sprites if sprite.rect.colliderect(self.player.hitbox)]
        if sprites:
            self.transition_target = sprites[0].target
            self.tint_mode = 'tint'

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and not self.dialog:
            closest_npc = None
            min_distance = float('inf')

            player_pos = pygame.math.Vector2(self.player.rect.center)
            for npc in self.npcs:
                npc_pos = pygame.math.Vector2(npc.rect.center)
                distance = player_pos.distance_to(npc_pos)

                if distance < min_distance:
                    min_distance = distance
                    closest_npc = npc

            if closest_npc and min_distance <= 180:
                if not closest_npc.dialog:
                    closest_npc.dialog = call_npc_engine_api(closest_npc.context['name'], closest_npc.context['desc'],
                                                             closest_npc.context['last_events'])

                    self.dialogs.append(closest_npc.dialog)

                self.dialog = Dialog(self.player, closest_npc, self.sprites, self.fonts['dialog'], self.on_dialog_end)
                self.player.blocked = True

        if keys[pygame.K_1]:
            # Good deeds for Sarah
            self.npcs[0].dialog = None
            self.npcs[0].context['last_events'] = [
                "Player completed a quest for Sarah to find a rare artifact that she was looking for for a long time.",
                "Player helped Sarah when she was attacked by bandits on the road.",
                "Player saved Sarah's brother's life during a war with enemy kingdom."
            ]
        elif keys[pygame.K_2]:
            # Bad deeds for Sarah
            self.npcs[0].dialog = None
            self.npcs[0].context['last_events'] = [
                "Player stole a rare artifact from Sarah and sold it to a local merchant who is Sarah's rival.",
                "Player denied to complete a quest for Sarah and instead helped her rival to complete the quest.",
                "Player joined the forces of the enemy country which led to Sarah's brother death in the battle killed by the player."
            ]
        elif keys[pygame.K_3]:
            # Good deeds for Anna
            self.npcs[1].dialog = None
            self.npcs[1].context['last_events'] = [
                "Player helped Anna to find a rare ingredient for her new potion.",
                "Player saved Anna's shop from a fire that was started by a group of bandits.",
            ]
        elif keys[pygame.K_4]:
            # Bad deeds for Anna
            self.npcs[1].dialog = None
            self.npcs[1].context['last_events'] = [
                "Player joined rival fraction of alchemists from the other town",
            ]
        elif keys[pygame.K_5]:
            # Good and bad deeds for John
            self.npcs[2].dialog = None
            self.npcs[2].context['last_events'] = [
                "Player helped John to find his lost dog.",
                "Player helped John to clean his house.",
                "Player stole a small amount of pretty common ore from John's chest.",
                "Player helped John to find a rare ore in the mine.",
                "Player lied to John during a trade and sold him a fake magic sword.",
            ]
        elif keys[pygame.K_6]:
            # Good deeds for Caroline
            self.npcs[3].dialog = None
            self.npcs[3].context['last_events'] = [
                "Player helped Caroline to find her lost child after he wandered into a dangerous forest.",
                "Player reunited Caroline with her missing husband, who had been captured by bandits.",
                "Player rescued Caroline's lost dog from a pack of wolves.",
                "Player defended Caroline’s farm from raiders trying to steal her livestock.",
                "Player helped Caroline rebuild her house after a devastating storm.",
                "Player nursed Caroline back to health after she fell ill with a rare disease.",
                "Player taught Caroline self-defense so she wouldn’t feel helpless in dangerous situations."
            ]
        elif keys[pygame.K_7]:
            # Bad deeds for Caroline
            self.npcs[3].dialog = None
            self.npcs[3].context['last_events'] = [
                "Player stole food from Caroline's farm, leaving her struggling to feed her family."
                "Player tricked Caroline into selling a family heirloom for a fraction of its value."
                "Player sabotaged Caroline's chances of receiving aid by spreading false rumors about her."
                "Player refused to help Caroline find her lost child, even when she begged for assistance."
            ]
        elif keys[pygame.K_8]:
            self.npcs[0].dialog = DIALOGUE_1
            self.npcs[1].dialog = DIALOGUE_7
            self.npcs[2].dialog = DIALOGUE_4
        elif keys[pygame.K_9]:
            self.npcs[0].dialog = DIALOGUE_2
            self.npcs[1].dialog = DIALOGUE_8
            self.npcs[2].dialog = DIALOGUE_5
        elif keys[pygame.K_0]:
            self.npcs[0].dialog = DIALOGUE_3
            self.npcs[1].dialog = DIALOGUE_9
            self.npcs[2].dialog = DIALOGUE_6

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

    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            self.display_surface.fill('black')

            for event in get_events():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            self.input()

            self.transition_check()
            self.sprites.update(dt)
            self.sprites.draw(self.player)

            if self.dialog: self.dialog.update()
            pygame.display.update()

            self.tint_screen(dt)


if __name__ == "__main__":
    game = Game()
    game.run()

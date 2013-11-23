#!/usr/bin/env python
import os
import pygame
from event import *
from main import *


space_dirs = {1: 'b_l', 2: 'b', 3: 'b_r', 4: 'l', 5: '', 6: 'r', 7: 't_l', 8: 't', 9: 't_r'}
player_idle = os.path.join('media/Player', 'Bob_Idle.png')
player_walk = os.path.join('media/Player', 'Bob_Walk.png')
player_run = os.path.join('media/Player', 'Bob_Run.png')


class BaseSprite(pygame.sprite.Sprite):

    def __init__(self):
        # Default sprite
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((42, 76))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()

        # Game properties
        self.world = None
        self.camera = None
        self.event = None

        # Animation properties
        self.direction = 'b_r'
        self.is_walking = False
        self.is_running = False
        self.is_aiming = False
        self.tiles = {}
        self.frame = 0

        # Movement properties
        self.speed = 0
        self.posX = None
        self.posY = None

    def get_all_tiles(self):
        for action in self.tiles:
            for filename in self.tiles[action]:
                actor, action_lower = filename.split('_')
                fo = open(os.path.join(self.tile_path, filename+'.txt'))
                for line in fo.readlines():
                    aLine = line.split(' = ')
                    direction = int(aLine[0].split('_'+action_lower+'_')[0].replace(actor+'_', ''))
                    step = int(aLine[0].split(actor+'_')[1].split('_'+action_lower+'_')[1])
                    aPos = aLine[1].split(' ')
                    if space_dirs[direction] not in self.tiles[action][filename]:
                        self.tiles[action][filename][space_dirs[direction]] = {}
                    self.tiles[action][filename][space_dirs[direction]][step] = {
                        'x': int(aPos[0]),
                        'y': int(aPos[1]),
                        'w': int(aPos[2]),
                        'h': int(aPos[3])
                    }

    def set_pos(self, x, y):
        # Center position of the sprite in the world
        self.rect.center = (x, y)

    def update(self):
        key = self.check_event()
        if key is None:
            self.is_walking = False
            self.image = pygame.image.load(player_idle).convert_alpha()
        else:
            self.is_walking = True
            if self.is_running:
                self.image = pygame.image.load(player_run).convert_alpha()
            else:
                self.image = pygame.image.load(player_walk).convert_alpha()
            self.direction = key

    def render(self):
        if not self.is_walking:
            actor = self.move('idle')
            self.speed = 0
        elif self.is_walking and not self.is_running:
            actor = self.move('walk')
            self.speed = WALK_SPEED
        else:
            actor = self.move('run')
            self.speed = RUN_SPEED
        self.image = self.image_at(actor, colorkey=(0, 0, 0))
        self.rect = self.image.get_rect()
        self.camera.screen.blit(self.image, (self.posX, self.posY))

    def move(self, action):
        self.frame += 1
        name_action = '{name}_{action}'.format(name=self.name, action=action.title())
        if self.frame not in self.tiles[action][name_action][self.direction]:
            self.frame = 0
        image = self.tiles[action][name_action][self.direction][self.frame]
        return (image['x'], image['y'], image['w'], image['h'])

    def image_at(self, rectangle, colorkey=None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.set_alpha(255)
        image.blit(self.image, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def check_event(self):
        pass


class Player(BaseSprite):

    def __init__(self):
        BaseSprite.__init__(self)
        self.name = 'Bob'
        self.category = CATEGORY.PLAYER
        self.tile_path = 'media/Player'
        self.tiles = {
            'idle': {'Bob_Idle': {}},
            'walk': {'Bob_Walk': {}},
            'run': {'Bob_Run': {}}
        }
        self.get_all_tiles()

    def set_start_pos(self):
        self.posX = WIDTH / 2
        self.posY = HEIGHT / 2
        self.set_pos(self.posX+(self.rect.width/2), self.posY+(self.rect.height/2))

    def update(self):
        BaseSprite.update(self)

    def check_event(self):
        Event(self.world, self)
        return self.event.listen_keys()

# -*- coding: utf-8 -*-

import os
import pygame
from settings import *
from utils import CATEGORY
from event import *


class BaseSprite(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.world = None
        self.image = None
        self.rect = None
        self.tmp_rect = None
        self.direction = None
        self.speed = 0
        self.is_moving = False
        self.is_runing = False
        self.is_aiming = False
        self.is_colliding = False
        self.tile_path = None
        self.tiles = None
        self.idle_tile = None
        self.walk_tile = None
        self.run_tile = None
        self.frame = 0
        self.pos_x = 0
        self.pos_y = 0

    def load_tiles(self):
        print('Loading sprites tiles for {}'.format(self.category))
        for action in self.tiles:
            for filename in self.tiles[action]:
                actor, action_lower = filename.split('_')
                fo = open(os.path.join(self.tile_path, filename+'.txt'))
                for line in fo.readlines():
                    aLine = line.split(' = ')
                    direction = int(aLine[0].split('_'+action_lower+'_')[0].replace(actor+'_', ''))
                    step = int(aLine[0].split(actor+'_')[1].split('_'+action_lower+'_')[1])
                    aPos = aLine[1].split(' ')
                    if SPACE_DIRECTIONS[direction] not in self.tiles[action][filename]:
                        self.tiles[action][filename][SPACE_DIRECTIONS[direction]] = {}
                    self.tiles[action][filename][SPACE_DIRECTIONS[direction]][step] = {
                        'x': int(aPos[0]),
                        'y': int(aPos[1]),
                        'w': int(aPos[2]),
                        'h': int(aPos[3])
                    }

    def set_pos(self, x, y):
        self.rect.left = self.pos_x = x
        self.rect.top = self.pos_y = y-self.world.camera.inset_y
        self.tmp_rect = self.rect

    def update(self):
        self.is_colliding = False

        key = self.check_event()
        if key is None:
            self.is_moving = False
            self.image = pygame.image.load(self.idle_tile).convert_alpha()
        else:
            self.is_moving = True
            if self.is_running:
                self.image = pygame.image.load(self.run_tile).convert_alpha()
            else:
                self.image = pygame.image.load(self.walk_tile).convert_alpha()
            self.direction = key

        if self.tmp_rect and self.world.screen and self.is_moving:
            collide = self.tmp_rect.collidelist(self.world.map.unwalkable)
            if collide > 0:
                self.is_colliding = True

    def check_event(self):
        pass

    def render(self):
        if not self.is_moving:
            actor = self.move('idle')
            self.speed = 0
        elif self.is_moving and not self.is_running:
            actor = self.move('walk')
            self.speed = WALK_SPEED
        else:
            actor = self.move('run')
            self.speed = RUN_SPEED
        self.image = self.image_at(actor, colorkey=(0, 0, 0))
        self.rect = self.image.get_rect()
        self.tmp_rect = self.rect.inflate(-10, -50)
        self.tmp_rect.left = HALF_WIDTH+self.tmp_rect.w/2
        self.tmp_rect.top = HALF_HEIGHT-self.tmp_rect.bottom

        if DEBUG:
            if self.world.screen:
                pygame.draw.rect(self.world.screen, (0, 0, 0), self.tmp_rect, 0)

        return (self.image, self.pos_x, self.pos_y)

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

    def get_reverse_direction(self, direction):
        reverse = {'t': 'b', 't_r': 'b_l', 'r': 'l', 'b_r': 't_l', 'b': 't', 'b_l': 't_r', 'l': 'r', 't_l': 'b_r'}
        return reverse[direction]

    def is_going_reverse(self, directions):
        for direction in directions.split(','):
            if self.direction == self.get_reverse_direction(direction):
                return True
        return False


class Player(BaseSprite):

    def __init__(self):
        BaseSprite.__init__(self)
        self.name = 'Bob'
        self.category = CATEGORY.PLAYER
        self.tile_path = PLAYER_DIR
        self.tiles = {
            'idle': {'Bob_Idle': {}},
            'walk': {'Bob_Walk': {}},
            'run': {'Bob_Run': {}}
        }
        self.load_tiles()
        self.idle_tile = PLAYER_IDLE
        self.walk_tile = PLAYER_WALK
        self.run_tile = PLAYER_RUN
        self.direction = 'b_r'
        self.visibility_w = 10
        self.visibility_l = 20

    def set_pos(self, x, y):
        BaseSprite.set_pos(self, x, y)

    def update(self):
        BaseSprite.update(self)

    def check_event(self):
        event = Event(self.world)
        return event.listen_keys()

    def visibility(self):
        return self.visibility_w, self.visibility_l

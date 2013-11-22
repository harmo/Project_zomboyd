#!/usr/bin/env python
import os
import pygame
from main import *


space_dirs = {1: 'b_l', 2: 'b', 3: 'b_r', 4: 'l', 5: '', 6: 'r', 7: 't_l', 8: 't', 9: 't_r'}

player_idle = os.path.join('media/Player', 'Bob_Idle.png')
player_walk = os.path.join('media/Player', 'Bob_Walk.png')
player_run = os.path.join('media/Player', 'Bob_Run.png')


class Player(object):

    def __init__(self, world):
        self.world = world
        self.name = 'Bob'
        self.direction = 'b_r'
        self.speed = 1
        self.posX = (self.world.num_tile_x/2)*self.world.dW
        self.posY = (self.world.num_tile_y/2)*self.world.tileHeight
        self.is_walking = False
        self.is_running = False
        self.is_aiming = False
        self.tile = None
        self.rect = None
        self.tile_path = 'media/Player'
        self.tiles = {
            'idle': {'Bob_Idle': {}},
            'walk': {'Bob_Walk': {}},
            'run': {'Bob_Run': {}}
        }

        self.get_tile_positions()

    def update(self, key):
        if key is None:
            self.is_walking = False
            self.sheet = pygame.image.load(player_idle).convert_alpha()
        else:
            self.is_walking = True
            if self.is_running:
                self.sheet = pygame.image.load(player_run).convert_alpha()
            else:
                self.sheet = pygame.image.load(player_walk).convert_alpha()
            self.direction = key

    def render(self, frame):
        if not self.is_walking:
            frame, player = self.move('idle', frame)
        elif self.is_walking and not self.is_running:
            frame, player = self.move('walk', frame)
        else:
            frame, player = self.move('run', frame)
        self.update_position()
        self.tile = self.image_at(player, colorkey=(0, 0, 0))
        self.rect = self.tile.get_rect()
        self.world.screen.blit(self.tile, (self.posX, self.posY))
        return frame

    def move(self, action, frame):
        frame += 1
        name_action = '{name}_{action}'.format(name=self.name, action=action.title())
        if frame not in self.tiles[action][name_action][self.direction]:
            frame = 0
        image = self.tiles[action][name_action][self.direction][frame]
        return frame, (image['x'], image['y'], image['w'], image['h'])

    def update_position(self):
        if self.is_walking:
            if self.is_running:
                self.speed = 2
            else:
                self.speed = 1

            Ymove = (self.world.dH/5) * self.speed
            Xmove = (self.world.dW/5) * self.speed

            if self.direction is 't':
                self.posY -= Ymove
            elif self.direction is 'b':
                self.posY += Ymove
            elif self.direction is 'l':
                self.posX -= Xmove
            elif self.direction is 'r':
                self.posX += Xmove
            elif self.direction is 't_l':
                self.posY -= Ymove
                self.posX -= Xmove
            elif self.direction is 't_r':
                self.posY -= Ymove
                self.posX += Xmove
            elif self.direction is 'b_l':
                self.posY += Ymove
                self.posX -= Xmove
            elif self.direction is 'b_r':
                self.posY += Ymove
                self.posX += Xmove

    def get_tile_positions(self):
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

    def image_at(self, rectangle, colorkey=None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.set_alpha(255)
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

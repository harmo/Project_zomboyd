# -*- coding: utf-8 -*-

import pygame
from settings import *
from utils import *


class Event(object):

    def __init__(self, world):
        self.world = world

    def listen_keys(self):
        if self.world:
            """ MOUSE EVENTS """
            if pygame.mouse.get_pressed()[0]:
                print('|| MOUSE ||')
                x, y = pygame.mouse.get_pos()
                x -= self.world.map.half_tile_width/2
                y += self.world.map.half_tile_height/2
                print('position : {0} / {1}'.format(x, y))
                xx, yy = self.world.get_cell(x, y)
                print('cells : {0} / {1}'.format(xx-1, yy-1))

            """ KEY EVENTS """
            keys_pressed = pygame.key.get_pressed()

            self.world.player.is_running = True if keys_pressed[pygame.K_LSHIFT] else False
            self.world.player.is_aiming = True if keys_pressed[pygame.K_LCTRL] else False

            if keys_pressed[pygame.K_RIGHT] and keys_pressed[pygame.K_DOWN]:
                return 'b_r'
            elif keys_pressed[pygame.K_RIGHT] and keys_pressed[pygame.K_UP]:
                return 't_r'
            if keys_pressed[pygame.K_LEFT] and keys_pressed[pygame.K_DOWN]:
                return 'b_l'
            elif keys_pressed[pygame.K_LEFT] and keys_pressed[pygame.K_UP]:
                return 't_l'
            if keys_pressed[pygame.K_RIGHT]:
                return 'r'
            elif keys_pressed[pygame.K_LEFT]:
                return 'l'
            if keys_pressed[pygame.K_UP]:
                return 't'
            elif keys_pressed[pygame.K_DOWN]:
                return 'b'
            return None

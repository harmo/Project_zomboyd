#!/usr/bin/env python
import pygame
from main import *


class Event(object):

    def __init__(self, world, player):
        self.world = world
        self.player = player
        self.player.event = self

    def listen_keys(self):
        """ MOUSE EVENTS """
        if pygame.mouse.get_pressed()[0]:
            print('|| MOUSE ||')
            x, y = pygame.mouse.get_pos()
            x -= (WIDTH/2)+self.world.map.dW
            print('{x} px / {y} px'.format(x=x, y=y))
            self.cell_x, self.cell_y = self.world.get_cell(x, y)
            print(self.cell_x, self.cell_y)
            self.world.set_property(self.cell_x, self.cell_y)
            print(self.world.cur_property)
            print(self.world.collide_prop)
            print('-----------')

            print('|| CAMERA ||')
            print(self.world.camera.cell_x, self.world.camera.cell_y)
            print('-----------')

        """ KEY EVENTS """
        keys_pressed = pygame.key.get_pressed()

        self.player.is_running = True if keys_pressed[pygame.K_LSHIFT] else False
        self.player.is_aiming = True if keys_pressed[pygame.K_LCTRL] else False

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

#!/usr/bin/env python
import pygame
from main import *


class Event(object):

    def __init__(self, player, world):
        self.player = player
        self.world = world

    def listen_keys(self, event):
        """ MOUSE EVENTS """
        x, y = pygame.mouse.get_pos()
        x -= (WIDTH/2)+self.world.dW
        self.tx, self.ty = self.screen_to_iso(x, y)

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

    def iso_to_screen(self, x, y):
        xx = (x-y)*self.world.dW
        yy = (x+y)*self.world.dH
        return xx, yy

    def screen_to_iso(self, x, y):
        xx = (y+(x/2))/self.world.tileWidth
        yy = (y-(x/2))/self.world.tileHeight
        return xx, yy

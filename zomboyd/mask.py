# -*- coding: utf-8 -*-

import pygame
from settings import *


class Mask(object):

    def __init__(self):
        self.surface = None
        self.rect = None
        self.direction = None
        self.rotation = 0

    def load_default(self):
        self.surface = pygame.image.load(MASK).convert()
        self.rect = self.surface.get_rect()

    def scale(self, visibility):
        self.surface = pygame.transform.scale(self.surface, (600, 1024))

    def rotate(self, direction):
        self.direction = direction
        self.rotation = self.get_degrees(direction)
        print(self.rotation)
        self.surface = pygame.transform.rotate(self.surface, self.rotation)

        self.surface.set_alpha(50)
        self.surface.set_colorkey((0, 0, 0), pygame.RLEACCEL)

        pixels = pygame.PixelArray(self.surface)
        pixels.replace((255, 255, 255), (1, 1, 1))
        self.surface.unlock()

        self.rect = self.surface.get_rect()

    def get_degrees(self, direction):
        directions = {'t': 180, 't_r': 135, 'r': 90, 'b_r': 45, 'b': 0, 'b_l': -45, 'l': -90, 't_l': -135}
        return directions[direction]

    def update(self, direction):
        if direction is not self.direction:
            self.rotate(direction)
            self.direction = direction

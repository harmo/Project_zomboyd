#!/usr/bin/env python
import pygame
from main import *


class Camera(object):

    def __init__(self):
        self.world = None
        self.screen = None
        self.offset = 40
        # the target that camera will move with
        self.target = None
        # used to translate object to be blited in camera
        self.cordX = 0
        self.cordY = 0
        self.minX = 0
        self.maxX = 0
        self.minY = 0
        self.maxY = 0

    def set_target(self, target):
        rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        self.target = target
        target.camera = self
        rect.center = self.target.rect.center
        self.cordX, self.cordY = rect.topleft

    def add_world(self, world):
        self.world = world

    def update(self):
        Xmove = (self.world.map.dW/5) * self.target.speed
        Ymove = (self.world.map.dH/5) * self.target.speed

        if self.target.direction is 't':
            self.cordY -= Ymove
        elif self.target.direction is 'b':
            self.cordY += Ymove
        elif self.target.direction is 'l':
            self.cordX -= Xmove
        elif self.target.direction is 'r':
            self.cordX += Xmove
        elif self.target.direction is 't_l':
            self.cordY -= Ymove
            self.cordX -= Xmove
        elif self.target.direction is 't_r':
            self.cordY -= Ymove
            self.cordX += Xmove
        elif self.target.direction is 'b_l':
            self.cordY += Ymove
            self.cordX -= Xmove
        elif self.target.direction is 'b_r':
            self.cordY += Ymove
            self.cordX += Xmove

        if self.screen:
            self.minX, self.maxX = self.world.screen_to_iso(self.cordX-WIDTH, self.cordX+WIDTH)
            self.minY, self.maxY = self.world.screen_to_iso(self.cordY-HEIGHT, self.cordY+HEIGHT)

    def render(self, screen, map):
        self.screen = screen
        posList = self.world.map.posList
        for layer in posList:
            for x in posList[layer]:
                if x >= self.minX-self.offset and x <= self.maxX+self.offset:
                    for y in posList[layer][x]:
                        if y >= self.minY-self.offset and y <= self.maxY+self.offset:
                            tile_x = posList[layer][x][y][0]-self.cordX
                            tile_y = posList[layer][x][y][1]-self.cordY
                            image = posList[layer][x][y][2]
                            screen.blit(image, (tile_x, tile_y))

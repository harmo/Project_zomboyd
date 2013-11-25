#!/usr/bin/env python
import pygame
from main import *


class Camera(object):

    def __init__(self):
        self.world = None
        self.screen = None
        # the target that camera will move with
        self.transX = 0
        self.transY = 0
        self.target = None
        # used to translate object to be blited in camera
        self.cordX = 0
        self.cordY = 0
        self.minX = 0
        self.maxX = 0
        self.minY = 0
        self.maxY = 0
        self.offset = 20
        self.x_offset = 0
        self.y_offset = 0
        self.cell_x = None
        self.cell_y = None

    def set_target(self, target):
        self.rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        self.target = target
        target.camera = self
        self.rect.center = self.target.rect.center
        self.cordX, self.cordY = (self.rect.left, self.rect.top)

    def add_world(self, world):
        self.world = world
        self.transX = 17
        self.transY = 17

    def update(self):
        if self.target.is_walking or not self.world.is_ready:
            if not self.target.is_collide():
                Xmove = (self.world.map.dW/5) * self.target.speed
                Ymove = (self.world.map.dH/5) * self.target.speed

                if self.target.direction is 't':
                    self.cordY -= Ymove
                    self.y_offset -= Ymove
                elif self.target.direction is 'b':
                    self.cordY += Ymove
                    self.y_offset += Ymove
                elif self.target.direction is 'l':
                    self.cordX -= Xmove
                    self.x_offset -= Xmove
                elif self.target.direction is 'r':
                    self.cordX += Xmove
                    self.x_offset += Xmove
                elif self.target.direction is 't_l':
                    self.cordY -= Ymove
                    self.cordX -= Xmove
                    self.x_offset -= Xmove
                    self.y_offset -= Ymove
                elif self.target.direction is 't_r':
                    self.cordY -= Ymove
                    self.cordX += Xmove
                    self.x_offset += Xmove
                    self.y_offset -= Ymove
                elif self.target.direction is 'b_l':
                    self.cordY += Ymove
                    self.cordX -= Xmove
                    self.x_offset -= Xmove
                    self.y_offset += Ymove
                elif self.target.direction is 'b_r':
                    self.cordY += Ymove
                    self.cordX += Xmove
                    self.x_offset += Xmove
                    self.y_offset += Ymove

                self.target.cordX = self.cordX
                self.target.cordY = self.cordY

                x, y = self.world.screen_to_iso(self.cordX+self.world.map.dW, self.cordY+self.world.map.dH)
                self.cell_x, self.cell_y = self.world.get_cell(x, y)
                self.world.set_property(self.cell_x+self.transX, self.cell_y+self.transY)

                self.minX, self.minY = (x-self.offset, y-self.offset)
                self.maxX, self.maxY = (x+self.offset*2, y+self.offset*2)

                if not self.world.is_ready:
                    self.world.is_ready = True

    def render(self, screen, map, layer, plan=None):
        self.screen = screen
        posList = self.world.map.posList
        for x in posList[layer]:
            if x >= self.minX and x <= self.maxX:
                for y in posList[layer][x]:
                    if y >= self.minY and y <= self.maxY:
                        tile_x = posList[layer][x][y][0]-self.cordX
                        tile_y = posList[layer][x][y][1]-self.cordY
                        if layer is BACKGROUND_LAYER:
                            image = posList[layer][x][y][2]
                            screen.blit(image, (tile_x, tile_y))
                        elif plan is 'first' and (y >= self.cell_y+self.transY or x >= self.cell_x+self.transX):
                            image = posList[layer][x][y][2]
                            screen.blit(image, (tile_x, tile_y))
                        elif plan is 'second' and (y < self.cell_y+self.transY or x < self.cell_x+self.transX):
                            image = posList[layer][x][y][2]
                            screen.blit(image, (tile_x, tile_y))

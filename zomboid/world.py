#!/usr/bin/env python
import os
from main import *
from vendor.pytmx import tmxloader


class World(object):

    def __init__(self, screen):
        self.screen = screen
        self.tmxMap = tmxloader.load_pygame(os.path.join("media/Map", "test.tmx"), pixelalpha=True)
        # self.tmxMap = tmxloader.load_pygame(os.path.join("graphics/zomboid", "test.tmx"), pixelalpha=True)
        self.num_tile_x = self.tmxMap.width
        self.tileWidth = self.tmxMap.tilewidth
        self.dW = self.tileWidth/2
        self.num_tile_y = self.tmxMap.height
        self.tileHeight = self.tmxMap.tileheight
        self.dH = self.tileHeight/2

    def iso_to_screen(self, x, y):
        xx = (x-y)*self.dW
        yy = (x+y)*self.dH
        return xx, yy

    def screen_to_iso(self, x, y):
        xx = (y+(x/2))/self.tileWidth
        yy = (y-(x/2))/self.tileHeight
        return xx, yy

    def render(self):
        for layer_index in range(len(self.tmxMap.layernames.keys())):
            for x in range(self.num_tile_x):
                for y in range(self.num_tile_y):
                    image = self.tmxMap.getTileImage(x, y, int(layer_index))
                    if image:
                        tile_x = ((x-y)*self.dW)+(WIDTH/2)
                        tile_y = ((x+y)*self.dH)
                        self.screen.blit(image, (tile_x, tile_y))

#!/usr/bin/env python
import os
from main import *
from vendor.pytmx import tmxloader


class Maps(object):

    def __init__(self, filename):
        self.tmxMap = tmxloader.load_pygame(os.path.join("media/Maps", filename), pixelalpha=True)
        # self.tmxMap = tmxloader.load_pygame(os.path.join("old/graphics/zomboid", filename), pixelalpha=True)
        self.num_tile_x = self.tmxMap.width
        self.tileWidth = self.tmxMap.tilewidth
        self.dW = self.tileWidth/2
        self.num_tile_y = self.tmxMap.height
        self.tileHeight = self.tmxMap.tileheight
        self.dH = self.tileHeight/2
        self.posList = {}

    def load(self):
        for layer_index in range(len(self.tmxMap.layernames.keys())):
            self.posList[layer_index] = {}
            for x in range(self.num_tile_x):
                self.posList[layer_index][x] = {}
                for y in range(self.num_tile_y):
                    image = self.tmxMap.getTileImage(x, y, int(layer_index))
                    if image:
                        self.posList[layer_index][x][y] = (((x-y)*self.dW)+(WIDTH/2), ((x+y)*self.dH), image)

    def get_pos(self, x, y, layer):
        return self.posList[layer][x][y][0], self.posList[layer][x][y][1]

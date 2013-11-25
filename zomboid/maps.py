#!/usr/bin/env python
import os
from main import *
from vendor.pytmx import tmxloader
from progressbar import *


class Maps(object):

    def __init__(self, filename):
        self.tmxMap = tmxloader.load_pygame(os.path.join("media/Maps", filename), pixelalpha=True)
        self.num_tile_x = self.tmxMap.width
        self.tileWidth = self.tmxMap.tilewidth
        self.dW = self.tileWidth/2
        self.num_tile_y = self.tmxMap.height
        self.tileHeight = self.tmxMap.tileheight
        self.dH = self.tileHeight/2
        self.posList = {}
        self.tile_properties = {}
        self.cell_numbers = {}
        self.cell_numbers_x = {}
        self.cell_numbers_y = {}

    def load(self):
        inc = 0
        progress = ProgressBar(maxval=self.num_tile_x*self.num_tile_y, widgets=[Percentage(), ' ', Bar(), ' ', ETA()])
        progress.start()
        for layer_index in range(len(self.tmxMap.layernames.keys())):
            self.posList[layer_index] = {}
            self.tile_properties[layer_index] = {}
            for x in range(self.num_tile_x):
                self.posList[layer_index][x] = {}
                for y in range(self.num_tile_y):
                    x_pos = ((x-y)*self.dW)+(WIDTH/2)
                    y_pos = ((x+y)*self.dH)

                    tile = self.tmxMap.getTileImage(x, y, int(layer_index))
                    if tile:
                        self.posList[layer_index][x][y] = (x_pos, y_pos, tile)

                    tile_property = self.tmxMap.getTileProperties((x, y, int(layer_index)))
                    if tile_property:
                        self.tile_properties[layer_index]['{x}_{y}'.format(x=x+1, y=y+1)] = tile_property

                    inc = inc + 1 if inc + 1 <= self.num_tile_x*self.num_tile_y else inc
                    progress.update(inc)
        progress.finish()

    def set_cell_numbers(self, cell_x, cell_y, x_pos, y_pos):
        for x in range(x_pos, x_pos+self.tileWidth):
            for y in range(y_pos, y_pos+self.tileHeight):
                index = '{x}_{y}'.format(x=x, y=y)
                self.cell_numbers[index] = (cell_x, cell_y)

    def get_pos(self, x, y, layer):
        return self.posList[layer][x][y][0], self.posList[layer][x][y][1]

    def get_properties(self, x, y, type):
        if type == 'collide':
            index = '{x}_{y}'.format(x=x, y=y)
            if index in self.tile_properties[WALL_LAYER]:
                return self.tile_properties[WALL_LAYER][index]
        return None

    def get_cell(self, x, y):
        index = '{x}_{y}'.format(x=x, y=y)
        return (self.cell_numbers[index])

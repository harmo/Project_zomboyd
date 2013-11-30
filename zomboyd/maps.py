# -*- coding: utf-8 -*-

import pygame
from vendor.pytmx import tmxloader
from progressbar import *
from settings import *
from utils import *


class Maps(object):

    def __init__(self, filename):
        self.tmxMap = tmxloader.load_pygame(project_path(MAPS_DIR, filename), pixelalpha=True)
        self.num_tile_x = self.tmxMap.width
        self.num_tile_y = self.tmxMap.height
        self.tile_width = self.tmxMap.tilewidth
        self.tile_height = self.tmxMap.tileheight
        self.half_tile_width = self.tile_width / 2
        self.half_tile_height = self.tile_height / 2

        self.positions_list = {}
        self.properties_list = {}
        self.unwalkable = []

    def load(self):
        inc = 0
        progress = ProgressBar(maxval=self.num_tile_x*self.num_tile_y, widgets=[Percentage(), ' ', Bar(), ' ', ETA()])
        progress.start()

        for layer_index in range(len(self.tmxMap.layernames.keys())):
            self.positions_list[layer_index] = {}
            self.properties_list[layer_index] = {}
            for x in range(self.num_tile_x):
                self.positions_list[layer_index][x] = {}
                self.properties_list[layer_index][x] = {}
                for y in range(self.num_tile_y):
                    tile_image = self.tmxMap.getTileImage(x, y, int(layer_index))
                    if tile_image:
                        # Set tiles positions
                        x_pos, y_pos = screen_to_iso(x, y, self.half_tile_width, self.half_tile_height)
                        self.positions_list[layer_index][x][y] = (x_pos, y_pos, tile_image)

                        tile_property = self.tmxMap.getTileProperties((x, y, int(layer_index)))
                        if tile_property:
                            self.properties_list[layer_index][x][y] = tile_property

                            # Set collisions tiles positions
                            if 'collide' in tile_property:
                                tmp_rect = pygame.Rect(x_pos, y_pos+self.tile_height, self.half_tile_width, self.half_tile_height)
                                old_bottom = tmp_rect.bottom
                                tmp_rect = tmp_rect.inflate(0, 10)
                                tmp_rect.bottom = old_bottom-10
                                self.unwalkable.append(tmp_rect)

                    inc = inc + 1 if inc + 1 <= self.num_tile_x*self.num_tile_y else inc
                    progress.update(inc)
        progress.finish()

    def get_properties(self, x, y, type):
        if type == 'collide':
            if x in self.properties_list[WALL_LAYER] and y in self.properties_list[WALL_LAYER][x]:
                if type in self.properties_list[WALL_LAYER][x][y]:
                    return self.properties_list[WALL_LAYER][x][y][type]
        return None

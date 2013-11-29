# -*- coding: utf-8 -*-

from settings import *
from utils import *


class World(object):

    def __init__(self):
        self.screen = None
        self.map = None
        self.camera = None
        self.player = None

    def add_map(self, map):
        self.map = map

    def add_player(self, player):
        self.player = player
        player.world = self

    def set_camera(self, camera):
        self.camera = camera
        camera.add_world(self)

    def update(self):

        self.player.update()

        if self.camera:
            self.camera.update()

    def render(self, screen):
        self.screen = screen
        if not (self.camera):
            raise Exception('No camera !')

        self.camera.render_map(screen, self.map)
        self.camera.render_player(screen, self.player)

    def get_cell(self, x, y):
        return iso_to_screen(x+self.camera.x_offset, y+self.camera.y_offset, self.map.half_tile_width, self.map.half_tile_height)

    def get_next_cell(self, x, y, direction):
        if direction in ['t', 't_r', 'r']:
            y -= 1
        elif direction in ['b', 'b_l', 'l']:
            y += 1
        if direction in ['l', 't_l', 't']:
            x -= 1
        elif direction in ['r', 'b_r', 'b']:
            x += 1
        return x, y

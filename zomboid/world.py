#!/usr/bin/env python
from main import *


class World(object):

    def __init__(self):
        self.is_ready = False
        self.entities = []
        self.camera = None
        self.map = None
        self.player = None
        self.cur_property = None
        self.collide_prop = None

    def add_map(self, map):
        self.map = map

    def add_entities(self, entity):
        # Entity should be a sprite class type
        self.entities.append(entity)
        entity.world = self

    def set_camera(self, camera):
        # Specify the camera that game is going to use to render the world
        self.camera = camera
        camera.add_world(self)

    def update(self):
        if self.entities:
            for entity in self.entities:
                entity.update()

        if self.camera:
            self.camera.update()

    def render(self, screen):
        if not (self.camera):
            raise Exception('No camera !')
        if not self.entities:
            raise Exception('No entity to render !')

        self.camera.render(screen, self.map, BACKGROUND_LAYER)
        self.camera.render(screen, self.map, WALL_LAYER, 'second')
        for entity in self.entities:
            entity.render()
        self.camera.render(screen, self.map, WALL_LAYER, 'first')

    def screen_to_iso(self, x, y):
        xx = (y+((x-self.map.dW)/2))/self.map.dW
        yy = (y-(x/2)-self.map.tileHeight)/self.map.tileHeight
        return int(xx), int(yy)

    def get_cell(self, x, y):
        x, y = (x+self.camera.x_offset, y+self.camera.y_offset)
        return self.screen_to_iso(x, y)

    def set_property(self, x, y):
        self.cur_property = self.map.get_properties(x, y, 'collide')
        if self.cur_property and 'collide' in self.cur_property:
            self.collide_prop = self.cur_property['collide'].split(',')

    def get_property(self, x, y):
        cur_property = self.map.get_properties(x, y, 'collide')
        if cur_property and 'collide' in cur_property:
            return cur_property['collide'].split(',')

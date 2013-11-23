#!/usr/bin/env python
from main import *


class World(object):

    def __init__(self):
        self.entities = []
        self.camera = None
        self.map = None
        self.player = None

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

        self.camera.render(screen, self.map)

        for entity in self.entities:
            entity.render()

    def iso_to_screen(self, x, y):
        xx = (x-y)*self.map.dW
        yy = (x+y)*self.map.dH
        return xx, yy

    def screen_to_iso(self, x, y):
        xx = (y+(x/2))/self.map.tileWidth
        yy = (y-(x/2))/self.map.tileHeight
        return xx, yy

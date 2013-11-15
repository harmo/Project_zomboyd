#!/usr/bin/env python


class World(object):

    def __init__(self):
        self.entities = []
        self.camera = None
        self.map = None
        self.player = None

    def addMap(self, map):
        self.map = map

    def update(self):
        if self.player:
            self.player.update()
        #check for any enities or update will be error
        if self.entities:
            for entity in self.entities:
                #check to update only the entities that is visible
                if self.camera:
                    translatedRect = self.camera.translate(entity.rect)
                    if (translatedRect.left <= -32 or translatedRect.right >= 672 or translatedRect.top <= -32 or translatedRect.bottom >= 512):
                        continue
                entity.update()
        if self.camera:
            self.camera.update()

    def render(self, surface):
        """use the specify camera to render all the entities onto the surface.
           Camera has to be set before usage.
        """
        #check if there is no camera is set, then do nothing
        if not (self.camera):
            print("No camera!")
            return

        #check the availibility of entities in the world
        if not self.entities:
            print("No entities to render")
            return

        #rendering entities according to camera cordinate
        #assuming background layer is index 0
        self.camera.render(surface, self.map, 0)
        for entity in self.entities:
            #check to render only the entities that is visible
            translatedRect = self.camera.translate(entity.rect)
            if (translatedRect.left <= -32 or translatedRect.right >= 672 or translatedRect.top <= -32 or translatedRect.bottom >= 512):
                continue
            surface.blit(entity.image, self.camera.translate(entity.rect))

        #after bliting all entities in the world, we blit the over layer on the top
        for layerIndex in xrange(1, len(self.map.tmxMap.layers)):
            if self.map.tmxMap.layers[layerIndex].name == "collision":
                continue
            self.camera.render(surface, self.map, layerIndex)

    def setCamera(self, camera):
        # Specify the camera that game is going to use to render the world
        self.camera = camera
        camera.addWorld(self)

    def addEntities(self, entity):
        # Entity should be a sprite class type
        self.entities.append(entity)
        entity.world = self

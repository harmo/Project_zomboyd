#!/usr/bin/env python
import os
import pygame
import sprite
import world
from map import Map


class Camera(object):

    def __init__(self):
        # used to translate object to be blited in camera
        self.cordX = 0
        self.cordY = 0
        # used to determine when to move the camera's cordinate
        self.windowX = 80
        self.windowY = 80
        # movement of camera
        self.dx = 0
        self.dy = 0

        self.world = None
        # the target that camera will move with
        self.follow = None

    def set_follow(self, sprite):
        rect = pygame.Rect(0, 0, 640, 480)
        self.follow = sprite
        rect.center = self.follow.rect.center
        self.cordX, self.cordY = rect.topleft

    def addWorld(self, world):
        self.world = world
        self.map_size_x = world.map.tmxMap.width * 32
        self.map_size_y = world.map.tmxMap.height * 32
        self.tile_pos_list = world.map.posList

    def translate(self, rect):
        return rect.move(-self.cordX, -self.cordY)

    def update(self):
        self.dx = self.follow.speed
        self.dy = self.follow.speed

        translatedRect = self.translate(self.follow.rect)
        if translatedRect.left <= self.windowX:
            self.cordX -= self.dx
        elif translatedRect.right >= 640 - self.windowX:
            self.cordX += self.dx
        if translatedRect.top <= self.windowY:
            self.cordY -= self.dy
        elif translatedRect.bottom >= 480 - self.windowY:
            self.cordY += self.dy

        self._check_bounder()

    def _check_bounder(self):
        if self.cordX < 0:
            self.cordX = 0
        elif self.cordX > self.map_size_x - 640:
            self.cordX = self.map_size_x - 640
        if self.cordY < 0:
            self.cordY = 0
        elif self.cordY > self.map_size_y - 480:
            self.cordY = self.map_size_y - 480

    def render(self, surface, worldMap, layer):
        top = 0 if self.cordY/32 < 0 else self.cordY/32
        bottom = (480+self.cordY)/32 + 1
        left = 0 if self.cordX/32 < 0 else self.cordX/32
        right = (640+self.cordX)/32 + 1

        for tile_y in self.tile_pos_list[top:bottom]:
            for tile_x in tile_y[left:right]:
                image = worldMap.getImage(tile_x[0]/32, tile_x[1]/32, layer)
                if image:
                    # There is no image at this location, so skip it
                    surface.blit(image, (tile_x[0]-self.cordX, tile_x[1]-self.cordY))


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Testing")
    clock = pygame.time.Clock()
    keepGoing = True

    worldMap = Map()
    worldMap.load(os.path.join("map", "test.tmx"))
    gameWorld = world.World()
    gameWorld.addMap(worldMap)

    player = sprite.Hero()
    player.load_sprite_sheet(os.path.join("graphics/Characters", "Actor1.png"), (32, 32), (0, 0), (96, 128))
    player.speed_is(3)
    player.walking_boundary_is(worldMap.size[0], worldMap.size[1])
    player.set_pos(200, 200)
    gameWorld.addEntities(player)

    cam = Camera()
    cam.set_follow(player)
    gameWorld.setCamera(cam)

    while keepGoing:
        clock.tick(32)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False

        gameWorld.update()
        gameWorld.render(screen)

        player.update()

        pygame.display.flip()

    pygame.quit()

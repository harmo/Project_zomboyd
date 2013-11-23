#!/usr/bin/env python
import pygame
from zomboid import *


WIDTH = 1280
HEIGHT = 1024
HALF_WIDTH = int(WIDTH / 2)
HALF_HEIGHT = int(HEIGHT / 2)
WALK_SPEED = 0.5
RUN_SPEED = 1

CATEGORIES = {
    'PLAYER': []
}


class Main(object):

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Testing")

        self.clock = pygame.time.Clock()
        self.state = True
        self.frame = 0

        ############################################

        self.map = Maps('test.tmx')
        self.map.load()
        self.world = World()
        self.world.add_map(self.map)
        self.player = Player()
        self.world.add_entities(self.player)
        self.player.set_start_pos()
        self.camera = Camera()
        self.camera.set_target(self.player)
        self.world.set_camera(self.camera)

        ############################################

        self.loop()

    def loop(self):
        while self.state:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = False

            self.world.update()
            self.world.render(self.screen)

            pygame.display.flip()
            self.clock.tick(12)
            # pygame.time.delay(100)


class Struct(object):
    def __init__(self, **entries):
        self.__dict__.update(entries)


def category():
    return Struct(**CATEGORIES)
CATEGORY = category()


if __name__ == '__main__':
    Main()

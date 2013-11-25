#!/usr/bin/env python
import pygame
from zomboid import *


MAIN_MAP = 'test_small.tmx'
# MAIN_MAP = 'test_huge.tmx'
# MAIN_MAP = 'test.tmx'
BACKGROUND_LAYER = 0
WALL_LAYER = 1
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
        print('Initialization...')
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Testing")
        self.bg_color = pygame.Color(0, 0, 0)

        self.clock = pygame.time.Clock()
        self.ON = True
        self.frame = 0

        print('Loading map tiles...')
        self.map = Maps(MAIN_MAP)
        self.map.load()
        print('Initialize world...')
        self.world = World()
        self.world.add_map(self.map)
        print('Initialize player...')
        self.player = Player()
        self.world.add_entities(self.player)
        self.player.set_start_pos()
        print('Initialize camera...')
        self.camera = Camera()
        self.world.set_camera(self.camera)
        self.camera.set_target(self.player)

        print('Launching game...')
        while self.ON:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.ON = False

            self.screen.fill(self.bg_color)
            self.world.update()
            self.world.render(self.screen)

            pygame.display.flip()
            self.clock.tick(15)
            # pygame.time.delay(500)


class Struct(object):
    def __init__(self, **entries):
        self.__dict__.update(entries)


def category():
    return Struct(**CATEGORIES)
CATEGORY = category()


if __name__ == '__main__':
    Main()

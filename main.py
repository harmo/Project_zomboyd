#!/usr/bin/env python
import pygame
from zomboid import *


WIDTH = 1280
HEIGHT = 1024


class Main(object):

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Testing")

        self.clock = pygame.time.Clock()
        self.state = True
        self.frame = 0

        self.world = World(self.screen)
        self.player = Player(self.world)
        self.event = Event(self.player, self.world)
        self.camera = Camera(self.world)

        self.loop()

    def loop(self):
        while self.state:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = False
                self.player.update(self.event.listen_keys(event))

            self.world.render()

            self.frame = self.player.render(self.frame)

            self.camera.update(self.player)

            pygame.display.flip()
            self.clock.tick(120)
            pygame.time.delay(100)

        self.state = False


if __name__ == '__main__':
    Main()

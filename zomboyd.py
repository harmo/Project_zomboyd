# -*- coding: utf-8 -*-

import pygame
import time
import ocempgui.widgets
from settings import *
from zomboyd import *


class Zomboyd:

    def __init__(self):
        self.screen = None
        self.bg_color = None
        self.run = True
        self.map = None
        self.world = None
        self.camera = None
        self.player = None
        self.mask = None
        self.font = None
        Zomboyd.instance = self

    @staticmethod
    def get_instance():
        return Zomboyd.instance

    def input(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.finish()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.finish()

    def finish(self):
        self.run = False

    def start(self, params=None):
        print('Initialization...')
        pygame.init()
        pygame.display.set_caption(VERSION_TITLE)
        # icon = pygame.image.load(ICON)
        # pygame.display.set_icon(icon)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.bg_color = pygame.Color(BG_COLOR[0], BG_COLOR[1], BG_COLOR[2])
        self.font = pygame.font.SysFont('mono', 10, bold=True)
        self.__loading_screen()

        print('Loading map...')
        self.map = Maps(MAIN_MAP)
        self.map.load()

        print('Initialize world...')
        self.world = World()
        self.world.add_map(self.map)

        print('Initialize player...')
        self.player = Player()
        self.player.update()
        self.world.add_player(self.player)

        print('Initialize camera...')
        self.camera = Camera()
        self.world.set_camera(self.camera)
        self.camera.render_player(self.screen, self.player)
        self.player.set_pos(HALF_WIDTH, HALF_HEIGHT)
        self.camera.set_target(self.player)

        self.init_game()

    def init_game(self):
        print('Launching game...')
        theClock = pygame.time.Clock()
        theClock_tick = theClock.tick
        # get_ticks = pygame.time.get_ticks
        time_sleep = time.sleep

        while self.run:
            self.input(pygame.event.get())

            time_sleep(0.01)
            theClock_tick(FPS)
            # now = get_ticks()
            # print(now)

            self.screen.fill(self.bg_color)
            self.world.update()
            self.world.render(self.screen)
            self.draw_text('FPS: {0}'.format(theClock.get_fps()))

            pygame.display.flip()

        self.run = False
        pygame.quit()

    def __loading_screen(self):
        widget_container = ocempgui.widgets.Renderer()
        widget_container.set_screen(self.screen)
        window = ocempgui.widgets.Box(60, 20)
        widget_container.color = (0, 0, 0)
        loading_label = ocempgui.widgets.Label('LOADING...')
        window.add_child(loading_label)
        window.topleft = LOADING_LABEL_POSITION
        widget_container.add_widget(window)

    def draw_text(self, text):
        fw, fh = self.font.size(text)
        surface = self.font.render(text, True, (0, 255, 0))
        self.screen.blit(surface, (20, 20))


if __name__ == "__main__":
    Zomboyd = Zomboyd()
    try:
        Zomboyd.start()
    except KeyboardInterrupt:
        print('\nExiting game...')

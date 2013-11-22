#!/usr/bin/env python
import pygame
from main import *


class Camera(object):

    def __init__(self, world):
        self.world = world
        self.follow = None
        self.cordX = 0
        self.cordY = 0
        # movement of camera
        self.dx = 0
        self.dy = 0

    def set_follow(self, player):
        rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        self.follow = player
        rect.center = self.follow.rect.center
        self.cordX, self.cordY = rect.topleft

    def translate(self, rect):
        return (rect.centerx-self.cordX, rect.centery-self.cordY)

    def update(self, player):
        self.set_follow(player)
        self.dx = self.follow.speed
        self.dy = self.follow.speed
        translatedRect = self.translate(self.follow.rect)
        print(translatedRect)
        # if translatedRect.left <= self.windowX:
        #     self.cordX -= self.dx
        # elif translatedRect.right >= WIDTH - self.windowX:
        #     self.cordX += self.dx
        # if translatedRect.top <= self.windowY:
        #     self.cordY -= self.dy
        # elif translatedRect.bottom >= HEIGHT - self.windowY:
        #     self.cordY += self.dy

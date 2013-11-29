# -*- coding: utf-8 -*-

import pygame
from settings import *
from utils import *


class Camera(object):

    def __init__(self):
        self.world = None
        self.target = None
        self.rect = None
        self.inset_y = 96
        self.x_offset = 0
        self.y_offset = 0

    def add_world(self, world):
        self.world = world

    def set_target(self, target):
        self.rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        self.target = target
        self.rect.center = self.target.rect.center

    def render_map(self, screen, map, layer, plane=None):
        def blit_tile(x, y, tile_x, tile_y):
            image = map.positions_list[layer][x][y][2]
            screen.blit(image, (tile_x, tile_y))

        for x in map.positions_list[layer]:
            for y in map.positions_list[layer][x]:
                tile_x = map.positions_list[layer][x][y][0]-self.rect.left
                tile_y = map.positions_list[layer][x][y][1]-self.rect.top/2-self.inset_y

                target_pos_y = HALF_HEIGHT-self.world.map.tile_height*2-self.target.rect.height

                if layer is BACKGROUND_LAYER:
                    blit_tile(x, y, tile_x, tile_y)
                elif plane is 'first' and (tile_y >= target_pos_y or x >= HALF_WIDTH):
                    blit_tile(x, y, tile_x, tile_y)
                elif plane is 'second' and (tile_y < target_pos_y or x < HALF_WIDTH):
                    blit_tile(x, y, tile_x, tile_y)

        if DEBUG:
            for collide in map.unwalkable:
                pygame.draw.rect(self.world.screen, (255, 255, 255), collide, 1)

    def render_player(self, screen, player):
        player_tile, player_x, player_y = player.render()
        screen.blit(player_tile, (player_x, player_y))

    def update(self):
        if self.target.is_moving:

            if self.target.is_colliding:
                xx, yy = self.world.get_cell(HALF_WIDTH, HALF_HEIGHT-self.world.map.tile_height*2)
                directions = self.world.map.get_properties(xx, yy, 'collide')
                if not directions:
                    # Wall cell is not on current cell, check next
                    next_x, next_y = self.world.get_next_cell(xx, yy, self.target.direction)
                    if self.world.map.get_properties(next_x, next_y, 'collide'):
                        return
                elif not self.target.is_going_reverse(directions):
                    return

            move_x, move_y = self.move()
            # Add moves to offsets, to keep coords real after moves
            self.x_offset -= move_x
            self.y_offset -= move_y

            # Update all collidable rects
            # TODO loop only on visible ones
            for collide in self.world.map.unwalkable:
                collide.left += move_x
                collide.top += move_y

    def move(self):
        origin_x, origin_y = self.rect.left, self.rect.top/2
        if self.target.direction == 't':
            self.rect.top -= self.target.speed
        elif self.target.direction == 'b':
            self.rect.top += self.target.speed
        elif self.target.direction == 'l':
            self.rect.left -= self.target.speed
        elif self.target.direction == 'r':
            self.rect.left += self.target.speed
        elif self.target.direction == 't_l':
            self.rect.top -= self.target.speed
            self.rect.left -= self.target.speed
        elif self.target.direction == 't_r':
            self.rect.top -= self.target.speed
            self.rect.left += self.target.speed
        elif self.target.direction == 'b_l':
            self.rect.top += self.target.speed
            self.rect.left -= self.target.speed
        elif self.target.direction == 'b_r':
            self.rect.top += self.target.speed
            self.rect.left += self.target.speed
        return (origin_x-self.rect.left, origin_y-self.rect.top/2)

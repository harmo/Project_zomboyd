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
        self.min_outset = 20
        self.max_outset = 25
        self.min_x = self.max_x = 0
        self.min_y = self.max_y = 0

    def add_world(self, world):
        self.world = world

    def set_target(self, target):
        self.rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        self.target = target
        self.rect.center = self.target.rect.center

    def update(self):
        if self.target.is_moving or not self.world.is_ready:
            xx, yy = self.world.get_cell(HALF_WIDTH, HALF_HEIGHT-self.world.map.tile_height*2)

            if self.target.is_colliding:
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

            self.min_x, self.min_y = xx-self.min_outset, yy-self.min_outset
            self.max_x, self.max_y = xx+self.max_outset, yy+self.max_outset

            # Update all collidable rects
            # TODO loop only on visible ones
            for collide in self.world.map.unwalkable:
                collide.left += move_x
                collide.top += move_y

            if not self.world.is_ready:
                self.world.is_ready = True

    def move(self):
        origin_x, origin_y = self.rect.left, self.rect.top/2

        if self.target.direction in ['t', 't_l', 't_r']:
            self.rect.top -= self.target.speed
        elif self.target.direction in ['b', 'b_l', 'b_r']:
            self.rect.top += self.target.speed
        if self.target.direction in ['l', 't_l', 'b_l']:
            self.rect.left -= self.target.speed
        elif self.target.direction in ['r', 't_r', 'b_r']:
            self.rect.left += self.target.speed

        return (origin_x-self.rect.left, origin_y-self.rect.top/2)

    def render_map(self, screen, map, layer, plane=None):
        def blit_tile(x, y, tile_x, tile_y):
            image = map.positions_list[layer][x][y][2]
            screen.blit(image, (tile_x, tile_y))

        for x in map.positions_list[layer]:
            if x >= self.min_x and x <= self.max_x:
                for y in map.positions_list[layer][x]:
                    if y >= self.min_y and y <= self.max_y:
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

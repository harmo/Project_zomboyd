# -*- coding: utf-8 -*-

import os


VERSION = '0.0.1'
VERSION_TITLE = 'Project Zomboyd v-{}'.format(VERSION)

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
path = lambda *a: os.path.join(*a)
project_path = lambda *a: os.path.join(PROJECT_ROOT, *a)

DEBUG = True
FPS = 15

MEDIAS = 'medias'
MAPS_DIR = os.path.join(MEDIAS, 'Maps')
MAIN_MAP = 'test_small.tmx'
# MAIN_MAP = 'test_huge.tmx'
# MAIN_MAP = 'test.tmx'
BG_COLOR = (0, 0, 0)
BACKGROUND_LAYER = 0
WALL_LAYER = 1
WIDTH = 1280
HEIGHT = 1024
HALF_WIDTH = int(WIDTH / 2)
HALF_HEIGHT = int(HEIGHT / 2)
WALK_SPEED = 2
RUN_SPEED = 5
LOADING_LABEL_POSITION = [HALF_WIDTH-20, HALF_HEIGHT-10]

SPACE_DIRECTIONS = {1: 'b_l', 2: 'b', 3: 'b_r', 4: 'l', 5: '', 6: 'r', 7: 't_l', 8: 't', 9: 't_r'}
PLAYER_DIR = os.path.join(MEDIAS, 'Player')
PLAYER_IDLE = os.path.join(PLAYER_DIR, 'Bob_Idle.png')
PLAYER_WALK = os.path.join(PLAYER_DIR, 'Bob_Walk.png')
PLAYER_RUN = os.path.join(PLAYER_DIR, 'Bob_Run.png')

CATEGORIES = {
    'PLAYER': []
}

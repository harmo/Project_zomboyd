# -*- coding: utf-8 -*-

from settings import *


def screen_to_iso(x, y, width, height):
    iso_x = ((x-y)*width)+HALF_WIDTH
    iso_y = (x+y)*height
    return iso_x, iso_y


def iso_to_screen(x, y, width, height):
    temp_x = (x-HALF_WIDTH)/width
    temp_y = y/height
    yy = (temp_y - temp_x)/2
    xx = temp_x + yy
    return int(xx), int(yy)


class Struct(object):
    def __init__(self, **entries):
        self.__dict__.update(entries)


def category():
    return Struct(**CATEGORIES)
CATEGORY = category()

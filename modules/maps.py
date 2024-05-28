#importing libs
import pygame
from modules.settings import *
from modules.blocks import *

pygame.init()

#making an array of map
def load_map(map_data, index):
    with open(map_data[index], "r") as file:
        data = file.read()
        return [[obj for obj in row] for row in data.splitlines()]

#drawing a map on the screen
def draw_map(map_list, w, h, sc):
    for y in range(len(map_list)):
        for x, value_x in enumerate(map_list[y]):
            if value_x == "1":
                block = Block(w * x, h * y, w, h, assets_blocks_data[0])
                block.draw(sc)
            elif value_x == "2":
                block = Block(w * x, h * y, w, h, assets_blocks_data[1])
                block.draw(sc)
            elif value_x == "3":
                block = Block(w * x, h * y, w, h, assets_blocks_data[2])
                block.draw(sc)
            elif value_x == "4":
                block = Block(w * x, h * y, w, h, assets_blocks_data[3])
                block.draw(sc)
            else: continue
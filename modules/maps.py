#importing libs
import pygame
import os
from modules.settings import assets_blocks_data
from modules.blocks import *

pygame.init()

#making an array of map
def load_map(maps, index, w, h):
    with open(maps[index], "r") as file:
        data = file.read()
        obj_list = [[obj for obj in row] for row in data.splitlines()]
        blocks = []
        for y in range(len(obj_list)):
            a = []
            for x, value_x in enumerate(obj_list[y]):
                if value_x == "1":
                    block = BrickWall(w * x, h * y, w, h, assets_blocks_data[0])
                    a.append(block)
                elif value_x == "2":
                    block = Block(w * x, h * y, w, h, assets_blocks_data[1])
                    a.append(block)
                elif value_x == "3":
                    block = TreeBlock(w * x, h * y, w, h, assets_blocks_data[2])
                    a.append(block)
                elif value_x == "4":
                    block = WaterBlock(w * x, h * y, w, h, assets_blocks_data[3])
                    a.append(block)
                else: a.append(None)
            blocks.append(a)

    return blocks

#drawing a map on the screen
def draw_map(blocks, sc):
    for row in blocks:
        for block in row:
            if block != None:
                block.draw(sc)
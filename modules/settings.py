#importing libs
import os
import pygame

pygame.init()

#variables
w, h = 800,600
w_s, h_s = 680, 600
x_select, y_select = w / 2 - 170, h / 2 + 50
fps = 24
level_number = 0
game = True
menu_show = True
game_over = False
win = False
final_score = 0

#list of blocks (brick wall, steel wall, tree, water)
assets_blocks_folder = os.path.join(os.path.dirname(__file__), "../assets/blocks")
assets_blocks_content = os.listdir(assets_blocks_folder)
assets_blocks_data = [os.path.join(assets_blocks_folder, file)
               for file in assets_blocks_content]

#assets folder
assets_folder = os.path.join(os.path.dirname(__file__), "../assets/")

#list of maps in .txt files
maps_folder = os.path.join(os.path.dirname(__file__), "../maps")
maps_content = os.listdir(maps_folder) 
map_data = [os.path.join(maps_folder, file) 
            for file in maps_content if file.endswith(".txt")]

#fonts
font = pygame.font.Font(os.path.join(assets_folder, "fonts/JoystixFont.ttf"), 24)
font2 = pygame.font.Font(os.path.join(assets_folder, "fonts/JoystixFont.ttf"), 16)

#groups
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
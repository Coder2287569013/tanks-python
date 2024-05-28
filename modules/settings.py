#importing libs
import os

#variables
w, h = 800,600
w_s, h_s = 680, 600
fps = 24
game = True

#list of blocks (brick wall, steel wall, tree, water)
assets_blocks_folder = os.path.join(os.path.dirname(__file__), "../assets/blocks")
assets_blocks_content = os.listdir(assets_blocks_folder)
assets_blocks_data = [os.path.join(assets_blocks_folder, file)
               for file in assets_blocks_content]

#list of maps in .txt files
maps_folder = os.path.join(os.path.dirname(__file__), "../maps")
maps_content = os.listdir(maps_folder) 
map_data = [os.path.join(maps_folder, file) 
            for file in maps_content if file.endswith(".txt")]
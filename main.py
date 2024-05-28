#importing libs
import pygame
from modules.settings import *
from modules.blocks import *
from modules.maps import *

pygame.init()

#The example of loading the map. Soon, it'll be different
level = load_map(map_data, 1)

#screen and clock
sc = pygame.display.set_mode((w, h))
surface_gameplay = pygame.Surface((w_s, h_s))
clock = pygame.time.Clock()

#main loop
while game:
    #drawing objects on display
    sc.fill((120, 120, 120))
    sc.blit(surface_gameplay, (0, 0))
    draw_map(level, 40, 40, surface_gameplay)

    #updating the screen and 
    pygame.display.update()

    #event processing
    for event in pygame.event.get():
        #1st event - exiting
        if event.type == pygame.QUIT:
            pygame.quit()
            game = False
    
    #set framerate
    clock.tick(fps)
#importing libs
import pygame
import os
from modules.maps import *
from modules.settings import *

pygame.init()

#screen and clock
sc = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()

#main loop
while game:
    #updating the screen
    pygame.display.update()

    #event processing
    for event in pygame.event.get():
        #1st event - exiting
        if event.type == pygame.QUIT:
            pygame.quit()
            game = False
    
    #set framerate
    clock.tick(fps)
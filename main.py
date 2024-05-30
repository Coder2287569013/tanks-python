import pygame
from modules.settings import *
from modules.blocks import *
from modules.maps import *
from modules.menu import *

pygame.init()

# The example of loading the map. Soon, it'll be different
level = load_map(map_data, 2)

# Screen and clock
sc = pygame.display.set_mode((w, h))
surface_gameplay = pygame.Surface((w_s, h_s))
clock = pygame.time.Clock()

# Main loop
while game:
    # Drawing objects on display
    if menu_show:
        # menu will be displayed if menu_show == True
        menu(sc, w, h, x_select, y_select)
    else:
        # drawing a map and other objects
        sc.fill((120, 120, 120))
        sc.blit(surface_gameplay, (0, 0))
        draw_map(level, 40, 40, surface_gameplay)
        
    # Updating the screen
    pygame.display.update()

    # Event processing
    for event in pygame.event.get():
        # Exiting
        if event.type == pygame.QUIT:
            game = False
            pygame.quit()
            break
        
        #use of K_DOWN and K_UP for the menu to select an option
        if event.type == pygame.KEYDOWN and menu_show:
            if event.key == pygame.K_DOWN:
                y_select = min(y_select + 70, h / 2 + 120)
            elif event.key == pygame.K_UP:
                y_select = max(y_select - 70, h / 2 + 50)
            elif event.key == pygame.K_RETURN:
                menu_show = False

    # Set framerate
    clock.tick(fps)
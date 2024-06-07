import pygame
from modules.settings import *
from modules.blocks import *
from modules.maps import *
from modules.menu import *
from modules.tank import *

pygame.init()

# The example of loading the map. Soon, it'll be different
level = load_map(map_data, 2, 40, 40)

# Screen and clock
sc = pygame.display.set_mode((w, h))
surface_gameplay = pygame.Surface((w_s, h_s))
clock = pygame.time.Clock()

enemy_tank = EnemyTank(200, 200, 34, 44, "tanks/enemy.png")
enemy_group.add(enemy_tank)
player = PlayerTank(200,560,34,42, "tanks/tank_player.png")
player_group.add(player) # Player position (example)

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
        surface_gameplay.fill((0, 0, 0))
        draw_water(level, surface_gameplay)
        bullet_group.draw(surface_gameplay)
        bullet_group.update(level)
        player_group.draw(surface_gameplay)
        player_group.update(level)
        enemy_group.draw(surface_gameplay)
        enemy_group.update((player.rect.x, player.rect.y), level)
        draw_map(level, surface_gameplay)
        
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
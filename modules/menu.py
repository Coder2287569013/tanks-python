import pygame
import os
from modules.settings import assets_folder, font

pygame.init()

logo_img = pygame.image.load(os.path.join(assets_folder, "icons/logo.png"))
logo_img = pygame.transform.scale(logo_img, (450, 150))

tank_img = pygame.image.load(os.path.join(assets_folder, "tanks/tank_player.png"))
tank_img = pygame.transform.scale(pygame.transform.rotate(tank_img, 270), (30, 24))

start_text = font.render('start game', True, (255, 255, 255))
select_text = font.render('select level', True, (255, 255, 255))

def menu(sc, w, h, x_select, y_select):
    sc.fill((0, 0, 0))
    sc.blit(logo_img, (w / 2 - 225, h / 2 - 200))
    sc.blit(start_text, (w / 2 - 100, h / 2 + 50))
    sc.blit(select_text, (w / 2 - 120, h / 2 + 120))
    sc.blit(tank_img, (x_select, y_select))
    
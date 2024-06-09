import pygame
import os
from modules.settings import assets_folder, font, level_number

pygame.init()

logo_img = pygame.image.load(os.path.join(assets_folder, "icons/logo.png"))
logo_img = pygame.transform.scale(logo_img, (450, 150))

tank_img = pygame.image.load(os.path.join(assets_folder, "tanks/tank_player.png"))
tank_img = pygame.transform.scale(pygame.transform.rotate(tank_img, 270), (30, 24))

game_over_sound = pygame.mixer.Sound(os.path.join(assets_folder, "sounds/gameover_sound.mp3"))
game_over_sound.set_volume(0.5)

start_text = font.render('start game', True, (255, 255, 255))
exit_text = font.render('exit', True, (255, 255, 255))
level_text = font.render(f'stage {level_number+1}', True, (0, 0, 0))
game_over_text = font.render('game over', True, (255, 255, 255))
win_text = font.render('you win!', True, (255, 255, 255))

def menu(sc, w, h, x_select, y_select):
    sc.fill((0, 0, 0))
    sc.blit(logo_img, (w / 2 - 225, h / 2 - 200))
    sc.blit(start_text, (w / 2 - 110, h / 2 + 50))
    sc.blit(exit_text, (w / 2 - 50, h / 2 + 120))
    sc.blit(tank_img, (x_select, y_select))

def lose(sc, w, h, game_over_sound_played):
    if not game_over_sound_played:
        game_over_sound.play()
        game_over_sound_played = True

    sc.fill((0, 0, 0))
    game_over_text_rect = game_over_text.get_rect(center=(w / 2, h / 2))
    sc.blit(game_over_text, game_over_text_rect)

    return game_over_sound_played

def win_sc(sc, w, h, win_sound, win_sound_played):
    if not win_sound_played:
        pygame.mixer.Sound(win_sound).play()
        win_sound_played = True

    sc.fill((0, 0, 0))
    win_text_rect = win_text.get_rect(center=(w / 2, h / 2))
    sc.blit(win_text, win_text_rect)

    return win_sound_played
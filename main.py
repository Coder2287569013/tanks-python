import pygame
import os
from modules.settings import *
from modules.blocks import *
from modules.maps import *
from modules.screens import *
from modules.tank import *
from modules.respawn import *

pygame.init()

# Load the map
level = load_map(map_data, 0, 40, 40)

# Sound
theme_sound = os.path.join(assets_folder, "sounds/theme_sound.mp3")

# Screen and clock
sc = pygame.display.set_mode((w, h))
pygame.display.set_caption("Battle City Python")
surface_gameplay = pygame.Surface((w_s, h_s))
clock = pygame.time.Clock()

player = PlayerTank(240, 560, 29, 37, "tanks/tank_player.png")
player_group.add(player)

# Variables for the sound and level start screen
theme_sound_played = False
theme_sound_duration = 0
game_over_sound_played = False
win_sound_played = False

# Main loop
while game:
    # Drawing objects on display
    if menu_show:
        # Menu will be displayed if menu_show == True
        menu(sc, w, h, x_select, y_select)
        pygame.mixer.music.stop()
        theme_sound_played = False
        game_over_sound_played = False  # Reset the game over sound flag

    if game_over:
        # Just game over
        game_over_sound_played = lose(sc, w, h, game_over_sound_played)
        pygame.mixer.music.stop()
        theme_sound_played = False
    
    if win:
        win_sound_played = win_sc(sc, w, h, theme_sound, win_sound_played)

    if not menu_show and not game_over and not win:
        score_text = font2.render(f"score", True, (0, 0, 0))
        score = font2.render(f"{final_score+player.score}", True, (0, 0, 0))
        hp_text = font2.render(f"hp", True, (0, 0, 0))
        hp = font2.render(f"{player.health}%", True, (0, 0, 0))
        stage_text = font2.render(f"stage {level_number+1}", True, (0, 0, 0))
        sc.fill((120, 120, 120))
        sc.blit(surface_gameplay, (0, 0))
        sc.blit(score_text, (w // 2 + 290, 100))
        sc.blit(score, (w // 2 + 290, 120))
        sc.blit(hp_text, (w // 2 + 290, 150))
        sc.blit(hp, (w // 2 + 290, 170))
        sc.blit(stage_text, (w // 2 + 290, h // 2))
        surface_gameplay.fill((0, 0, 0))
        draw_water(level, surface_gameplay)
        player_group.draw(surface_gameplay)
        enemy_group.draw(surface_gameplay)
        draw_map(level, surface_gameplay)
        bullet_group.draw(surface_gameplay)

        if not theme_sound_played:
            pygame.mixer.music.load(theme_sound)
            pygame.mixer.music.play()
            theme_sound_played = True
            theme_sound_duration = pygame.time.get_ticks() + 4000

        if pygame.time.get_ticks() >= theme_sound_duration:
            player_group.update(level)
            enemy_group.update((player.rect.centerx, player.rect.centery), level)
            bullet_group.update(level)
            respawn()

        if player.health <= 0:
            game_over = True

        if player.score >= 1000:
            if level_number < len(map_data) - 1:
                final_score += player.score
                level_number += 1
                player.rect.x, player.rect.y = 240, 560
                player.direction = "up"
                player.health = 100
                theme_sound_played = False
                level = load_map(map_data, level_number, 40, 40)
                bullet_group.empty()
                enemy_group.empty()
                player.score = 0
            else:
                win = True

    # Updating the screen
    pygame.display.update()

    # Event processing
    for event in pygame.event.get():
        # Exiting
        if event.type == pygame.QUIT:
            game = False
            pygame.quit()
            break

        # Use of K_DOWN and K_UP for the menu to select an option
        if event.type == pygame.KEYDOWN and menu_show:
            if event.key == pygame.K_DOWN:
                y_select = min(y_select + 70, h / 2 + 120)
            elif event.key == pygame.K_UP:
                y_select = max(y_select - 70, h / 2 + 50)
            elif event.key == pygame.K_RETURN:
                if y_select >= h / 2 + 120:
                    game = False
                    pygame.quit()
                    break
                else:
                    menu_show = False

    # Set framerate
    clock.tick(fps)
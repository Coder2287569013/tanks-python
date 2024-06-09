import pygame
import random
from modules.tank import EnemyTank
from modules.settings import enemy_group

pygame.init()

countdown = 120

def respawn():
    global countdown
    if countdown > 0:
        countdown -= 1
    else:
        enemy = EnemyTank(random.choice([240, 360]), 0, 29, 39, "tanks/enemy.png")
        enemy_group.add(enemy)
        countdown = 120
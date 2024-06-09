import pygame
import os
import random
from modules.settings import assets_folder, bullet_group, w_s, h_s, player_group
from modules.bullet import Bullet
from modules.blocks import *


pygame.init()
pygame.mixer.init()

sound_playing = False
moving_sound = pygame.mixer.Sound(os.path.join(assets_folder, "sounds/moving_sound.mp3"))
shooting_sound = pygame.mixer.Sound(os.path.join(assets_folder, "sounds/shooting_sound.mp3"))

class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, image):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.transform.scale(
            pygame.image.load(os.path.join(assets_folder, image)),
            (w, h)
        )
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.direction = "down"
        self.move_delay = 0
        self.shoot_delay = 0
        self.aligned = False
        self.health = 100
        self.directions = {
            "left": (-self.speed, 0),
            "right": (self.speed, 0),
            "up": (0, -self.speed),
            "down": (0, self.speed)
        }
    
    def shoot(self):
        position = {
            "left": (self.rect.left-15, self.rect.centery),
            "right": (self.rect.right+15, self.rect.centery),
            "up": (self.rect.centerx, self.rect.top-15),
            "down": (self.rect.centerx, self.rect.bottom+15)
        }[self.direction]
        bullet = Bullet(position[0], position[1], 7, 23, self.direction)
        bullet_group.add(bullet)
        shooting_sound.play()

    def move(self, level):
        dx, dy = self.directions[self.direction]
        if not self.check_collision(dx, dy, level, w_s, h_s):
            self.rect.x += dx
            self.rect.y += dy
        else:
            self.direction = random.choice(["left", "right", "up", "down"])
            self.rotate(self.direction)

    def choose_direction(self, player_pos, level):
        player_x, player_y = player_pos[0] // 40, player_pos[1] // 40
        tank_x, tank_y = self.rect.x // 40, self.rect.y // 40

        if abs(player_x - tank_x) > abs(player_y - tank_y):
            if player_x < tank_x:
                self.direction = "left"
            else:
                self.direction = "right"
        else:
            if player_y < tank_y:
                self.direction = "up"
            else:
                self.direction = "down"

    def check_collision(self, dx, dy, level, w_s, h_s):
        next_rect = self.rect.move(dx, dy)
        for row in level:
            for block in row:
                if isinstance(block, (BrickWall, SteelWall, WaterBlock)) and next_rect.colliderect(block.rect):
                    return True
        if next_rect.left <= 0 or next_rect.right >= w_s or next_rect.bottom >= h_s or next_rect.top <= 0:
            return True
        return False

    def check_alignment(self, player_pos, level):
        player_x, player_y = player_pos[0], player_pos[1]
        enemy_x, enemy_y = self.rect.centerx, self.rect.centery
        tolerance = 5

        if abs(enemy_x - player_x) <= tolerance:
            y_min, y_max = sorted([int(enemy_y // 40), int(player_y // 40)])
            for y in range(y_min + 1, y_max):
                if 0 <= y < len(level) and 0 <= int(enemy_x // 40) < len(level[y]):
                    if isinstance(level[y][int(enemy_x // 40)], (BrickWall, SteelWall)):
                        return False
            return True

        if abs(enemy_y - player_y) <= tolerance:
            x_min, x_max = sorted([int(enemy_x // 40), int(player_x // 40)])
            for x in range(x_min + 1, x_max):
                if 0 <= int(enemy_y // 40) < len(level) and 0 <= x < len(level[int(enemy_y // 40)]):
                    if isinstance(level[int(enemy_y // 40)][x], (BrickWall, SteelWall)):
                        return False
            return True

        return False

    def rotate(self, direction):
        angle = {
            "left": 90,
            "right": -90,
            "up": 0,
            "down": 180
        }[direction]
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)


class PlayerTank(Tank):
    def __init__(self, x, y, w, h, image):
        super().__init__(x, y, w, h, image)
        self.direction = "up"
        self.score = 0

    def update(self, level):
        keys = pygame.key.get_pressed()
        self.handle_input(keys, level)
        if keys[pygame.K_SPACE] and self.shoot_delay <= 0:
            self.shoot()
            self.shoot_delay = 20

        if self.shoot_delay > 0:
            self.shoot_delay -= 1

        if self.health <= 0:
            self.kill()
    

    def handle_input(self, keys, level):
        moving = False
        if keys[pygame.K_LEFT]:
            self.direction = "left"
            moving = True
        elif keys[pygame.K_RIGHT]:
            self.direction = "right"
            moving = True
        elif keys[pygame.K_UP]:
            self.direction = "up"
            moving = True
        elif keys[pygame.K_DOWN]:
            self.direction = "down"
            moving = True

        if moving:
            self.move(level)
            self.rotate(self.direction)

    def move(self, level):
        dx, dy = self.directions[self.direction]
        if not self.check_collision(dx, dy, level, w_s, h_s):
            self.rect.x += dx
            self.rect.y += dy

class EnemyTank(Tank):
    def __init__(self, x, y, w, h, image):
        super().__init__(x, y, w, h, image)
        self.spawn_cooldown = 10 
        self.safe_position_reached = False 

    def update(self, player_pos, level):
        if self.spawn_cooldown > 0:
            self.spawn_cooldown -= 1
            return

        self.aligned = self.check_alignment(player_pos, level)
        if self.aligned:
            self.choose_direction(player_pos, level)
            self.rotate(self.direction)
            if self.shoot_delay <= 0:
                self.shoot()
                self.shoot_delay = 30
        else:
            if self.move_delay <= 0:
                self.move_delay = random.randint(20, 60)
                self.choose_direction(player_pos, level)
                self.rotate(self.direction)
            else:
                self.move_delay -= 1
            self.move(level)
        
        if self.shoot_delay > 0:
            self.shoot_delay -= 1
        
        if self.health <= 0:
            self.kill()
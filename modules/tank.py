import pygame
import os
import random
from modules.settings import assets_folder, bullet_group
from modules.bullet import Bullet
from modules.blocks import BrickWall


pygame.init()

class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, image):
        super().__init__()
        self.original_image = pygame.transform.scale(
            pygame.image.load(os.path.join(assets_folder, image)),
            (w, h)
        )
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.direction = random.choice(["left", "right", "up", "down"])
        self.move_delay = 0
        self.shoot_delay = 0
        self.aligned = False

    def update(self, player_pos, level):
        self.aligned = self.check_alignment(player_pos, level)
        if self.aligned:
            self.choose_direction(player_pos)
            self.rotate()
            if self.shoot_delay <= 0:
                self.shoot()
                self.shoot_delay = 30
        else:
            if self.move_delay <= 0:
                self.move_delay = random.randint(20, 60)
                self.choose_direction(player_pos)
                self.rotate()
            else:
                self.move_delay -= 1
            self.move(level)
        
        if self.shoot_delay > 0:
            self.shoot_delay -= 1
    
    def shoot(self):
        position = {
            "left": (self.rect.left, self.rect.centery),
            "right": (self.rect.right, self.rect.centery),
            "up": (self.rect.centerx, self.rect.top),
            "down": (self.rect.centerx, self.rect.bottom)
        }[self.direction]
        bullet = Bullet(position[0], position[1], 7, 23, self.direction)
        bullet_group.add(bullet)

    def move(self, level):
        directions = {
            "left": (-self.speed, 0),
            "right": (self.speed, 0),
            "up": (0, -self.speed),
            "down": (0, self.speed)
        }
        dx, dy = directions[self.direction]
        if not self.check_collision(dx, dy, level):
            self.rect.x += dx
            self.rect.y += dy
        else:
            self.direction = random.choice(["left", "right", "up", "down"])
            self.rotate()

    def choose_direction(self, player_pos):
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

    def check_collision(self, dx, dy, level):
        next_rect = self.rect.move(dx, dy)
        for row in level:
            for block in row:
                if isinstance(block, BrickWall) and next_rect.colliderect(block.rect):
                    return True
        return False

    def check_alignment(self, player_pos, level):
        player_x, player_y = player_pos[0] // 40, player_pos[1] // 40
        enemy_x, enemy_y = self.rect.x // 40, self.rect.y // 40

        if enemy_x == player_x:
            y_min, y_max = sorted([enemy_y, player_y])
            for y in range(y_min + 1, y_max):
                if isinstance(level[y][enemy_x], BrickWall):
                    return False
            return True

        if enemy_y == player_y:
            x_min, x_max = sorted([enemy_x, player_x])
            for x in range(x_min + 1, x_max):
                if isinstance(level[enemy_y][x], BrickWall):
                    return False
            return True

        return False

    def rotate(self):
        angle = {
            "left": 90,
            "right": -90,
            "up": 0,
            "down": 180
        }[self.direction]
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)
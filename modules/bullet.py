import pygame
import os
from modules.settings import assets_folder
from modules.blocks import BrickWall

pygame.init()

bullet_img = pygame.image.load(os.path.join(assets_folder, "icons/image.png"))

#Bullet class and it's methods
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 2
        self.image = pygame.transform.rotate(bullet_img, 270)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.direction = direction
        self.direction_map = {
            "left": (-self.speed, 0),
            "right": (self.speed, 0),
            "up": (0, -self.speed),
            "down": (0, self.speed)
        }

    def update(self, level):
        dx, dy = self.direction_map.get(self.direction)

        self.rect.x += dx
        self.rect.y += dy

        self.check_collision(level)

    def check_collision(self, level):
        for row in level:
            for block in row: 
                if isinstance(block, BrickWall) and self.rect.colliderect(block.rect):
                    block.change_image(self.direction)
                    self.kill()  

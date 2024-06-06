import pygame
import os
from modules.settings import assets_folder
from modules.blocks import BrickWall

pygame.init()

bullet_img = pygame.image.load(os.path.join(assets_folder, "icons/image.png"))

#Bullet class and it's methods
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 2
        self.direction_map = {
            "left": ((-self.speed, 0), 90),
            "right": ((self.speed, 0), -90),
            "up": ((0, -self.speed), 0),
            "down": ((0, self.speed), 180)
        }
        self.direction = direction
        self.original_image = pygame.transform.scale(bullet_img, (w, h))
        self.image = pygame.transform.rotate(
            self.original_image.copy(), self.direction_map[self.direction][1]
        )
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
    def update(self, level):
        dx, dy = self.direction_map[self.direction][0]

        self.rect.x += dx
        self.rect.y += dy

        self.check_collision(level)

    def check_collision(self, level):
        for row in level:
            for block in row: 
                if isinstance(block, BrickWall) and self.rect.colliderect(block.rect):
                    if block.hit < 1:
                        block.change_image(self.direction)
                        block.hit += 1
                    else: row.remove(block)
                    self.kill()
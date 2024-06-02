#importing libs
import pygame

pygame.init()

#Main class of blocks: class Block. Every block will be inheriting from it
class Block():
    def __init__(self, x, y, w, h, img):
        self.rect = pygame.Rect(x, y, w, h)
        self.img = pygame.transform.scale(pygame.image.load(img), 
                   (self.rect.width, self.rect.height))
    
    def draw(self, sc):
        sc.blit(self.img, (self.rect.x, self.rect.y))

#This is gonna be later...
class BrickWall(Block):
    def __init__(self, x, y, w, h, img):
        super().__init__(x, y, w, h, img)
        self.original_img = self.img.copy()
        self.hit = False

    def change_image(self, direction):
        if direction == "left":
            self.img = self.original_img.subsurface((0, 0, self.rect.width // 2, self.rect.height))
        elif direction == "right":
            self.img = self.original_img.subsurface((self.rect.width // 2, 0, self.rect.width // 2, self.rect.height))
            self.rect.x += self.rect.width // 2
        elif direction == "up":
            self.img = self.original_img.subsurface((0, 0, self.rect.width, self.rect.height // 2))
        elif direction == "down":
            self.img = self.original_img.subsurface((0, self.rect.height // 2, self.rect.width, self.rect.height // 2))
            self.rect.y += self.rect.height // 2

# class SteelWall(Block):
#     def __init__(self, x, y, w, h, img):
#         super().__init__(x, y, w, h, img)


# class WaterBlock(Block):
#     def __init__(self, x, y, w, h, img):
#         super().__init__(x, y, w, h, img)


# class TreeBlock(Block):
#     def __init__(self, x, y, w, h, color):
#         super().__init__(x, y, w, h, color)
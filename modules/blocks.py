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
# class BrickWall(Block):
#     def __init__(self, x, y, w, h, img):
#         super().__init__(x, y, w, h, img)


# class SteelWall(Block):
#     def __init__(self, x, y, w, h, img):
#         super().__init__(x, y, w, h, img)


# class WaterBlock(Block):
#     def __init__(self, x, y, w, h, img):
#         super().__init__(x, y, w, h, img)


# class TreeBlock(Block):
#     def __init__(self, x, y, w, h, color):
#         super().__init__(x, y, w, h, color)
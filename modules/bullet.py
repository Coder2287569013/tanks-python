import pygame
import os
from modules.settings import assets_folder, player_group, enemy_group, w_s, h_s
from modules.blocks import BrickWall, SteelWall

pygame.init()
pygame.mixer.init()

bullet_img = pygame.image.load(os.path.join(assets_folder, "icons/image.png"))
boom_sound = pygame.mixer.Sound(os.path.join(assets_folder, "sounds/boom_sound.mp3"))
animation_imgs = [pygame.transform.scale(
                  pygame.image.load(os.path.join(assets_folder, f"animation/explosion{i+1}.png")), 
                  (150, 150)) for i in range(13)]

# Bullet class and its methods
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
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
        self.animation_index = 0
        self.animation_rate = 2  
        self.animation_counter = 0
        self.animating = False
        self.sound_played = False
        self.hit_target = False 

    def update(self, level):
        if not self.animating:
            dx, dy = self.direction_map[self.direction][0]
            self.rect.x += dx
            self.rect.y += dy
            self.check_collision(level, w_s, h_s)
        else:
            self.play_animation()

    def play_animation(self):
        if not self.sound_played:
            boom_sound.play()
            self.sound_played = True
        if self.animation_counter % self.animation_rate == 0:
            if self.animation_index < len(animation_imgs):
                self.image = animation_imgs[self.animation_index]
                self.rect = self.image.get_rect(center=self.rect.center) 
                self.animation_index += 1
            else:
                self.kill()
        self.animation_counter += 1

    def check_collision(self, level, w_s, h_s):
        if self.animating:
            return

        if self.rect.right < 0 or self.rect.left > w_s or self.rect.top > h_s or self.rect.bottom < 0:
            self.kill()

        for player in player_group:
            if self.rect.colliderect(player.rect):
                player.health -= 10
                self.hit_target = True
                self.start_animation()
                return  
            
        for enemy in enemy_group:
            if self.rect.colliderect(enemy.rect):
                enemy.health -= 100
                player.score += 100
                self.hit_target = True
                self.start_animation()
                return

        for row in level:
            for block in row:
                if block is not None and self.rect.colliderect(block.rect):
                    if isinstance(block, BrickWall):
                        if block.hit < 1:
                            block.change_image(self.direction)
                            block.hit += 1
                        else:
                            row.remove(block)
                        self.start_animation()
                    if isinstance(block, SteelWall):
                        self.start_animation()
                    return    

    def start_animation(self):
        self.animating = True
        self.animation_index = 0
        self.animation_counter = 0
        self.sound_played = False
        self.image = animation_imgs[self.animation_index]
        self.rect = self.image.get_rect(center=self.rect.center)
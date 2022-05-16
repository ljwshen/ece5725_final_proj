import os
from tkinter import Widget
import random
import pygame
from pygame.locals import *
from constants import *


images = [pygame.image.load('directions/left.png'),
          pygame.image.load('directions/right.png'),
          pygame.image.load('directions/up.png'),
          pygame.image.load('directions/down.png')]

missed_img = pygame.image.load('directions/hit.png')

hit_images = [pygame.image.load('cut_half/left.jpg'),
              pygame.image.load('cut_half/right.jpg'),
              pygame.image.load('cut_half/up.jpg'),
              pygame.image.load('cut_half/down.jpg')]

class Arrow(pygame.sprite.Sprite):
    def __init__(self, image_key):
        super(Arrow, self).__init__()
        # print("genreating arrow", image_key)
        self.key = image_key
        img = images[image_key]
        self.image = pygame.transform.scale(img, (20, 20))
            
        self.hit = False
        self.rect = self.image.get_rect()
        self.rect.y = 0 #starting low for testing purposes
        self.rect.x = random.randrange(0+20, width-20)

    def arrow_move(self, speed):
        self.rect = self.rect.move(speed)
        if self.rect.bottom > 235 and not self.hit:
            self.image = pygame.transform.scale(missed_img, (20, 20))
        elif self.rect.bottom > height:
            self.kill()

    def arrow_hit(self):
        self.hit = True
        self.image = pygame.transform.scale(hit_images[self.key], (35, 35))


def GetDirArrow():
    image_key = random.randint(0, 3)
    return Arrow(image_key)

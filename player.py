import pygame
from pygame.locals import *
PLAYER_WIDTH=20

class Cursor(object):
    """cursor object"""

    def __init__(self,x,y):
        """
        initialize cursor
        parameter x: x position of cursor
        parameter y: x position of cursor
        """
        self.image = pygame.transform.scale(pygame.image.load('cursor.png'), (PLAYER_WIDTH,PLAYER_WIDTH))
        self.x=x #x pos of cursor
        self.y=y #y pos of cursor
    
    def draw(self):
      #display player on screen
      screen.blit(self.image, (self.x-PLAYER_WIDTH/2,self.y-PLAYER_WIDTH/2))


import pygame

PLAYER_WIDTH=20

cursor_images = [pygame.image.load('cursor/cursor_l.png'),
                 pygame.image.load('cursor/cursor_r.png'),
                 pygame.image.load('cursor/cursor_u.png'),
                 pygame.image.load('cursor/cursor_d.png'),
                 pygame.image.load('cursor/cursor.png'),]


class Cursor(object):
    """cursor object"""

    def __init__(self,x,y):
        """
        param x: x position of center
        param y: y position of center
        """
        self.x=x
        self.y = y
        self.image = pygame.transform.scale(pygame.image.load('cursor/cursor.png'), (PLAYER_WIDTH,PLAYER_WIDTH))
        
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, (self.x-PLAYER_WIDTH/2,self.y-PLAYER_WIDTH/2))
    
    def set_dir(self, direction):
        self.image = pygame.transform.scale(cursor_images[direction], (PLAYER_WIDTH+10,PLAYER_WIDTH+10))
        



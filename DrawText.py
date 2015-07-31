import pygame


from pygame.locals import *


class DrawText:
    def __init__(self, width, height):
        self.width  = width
        self.height = height
        self.size = self.width, self.height

    def on_init(self):
        self.font = pygame.font.SysFont(None, 20)
    
    def on_render(self, screen, text, positionH ='middle', positionW ='middle'):
        fw, fh = self.font.size(text)
        surface = self.font.render(text, True, (0,255,0))
        if positionH=='middle':
            positiony = (self.height - fh)/2
            
        if positionW=='middle':
            positionx = (self.width- fw)/2
        
        if positionH== 'top':
            positiony = fh /2
        elif positionH == 'bottom':
            positiony = self.height - (fh)
        if positionW== 'left':
            positionx = fw /2
        elif positionW == 'right':
            positionx = self.width - fw          
        screen.blit(surface, (positionx, positiony ))
        
    def on_cleanup(self):
         pass
        

import pygame
from pygame.locals import *
import gopigo

class Sensor_UltraSound:
    def __init__(self):
        self._usdist = False
        self.dist = 0
    def on_init(self):        
       pass
    def on_start_stop_usdist(self):
        self._usdist = not self._usdist
        
    def on_loop(self):
        if self._usdist:
            self.dist = gopigo.us_dist(15)      
    def on_render(self,screen,drawtext):
        if self._usdist:
            drawtext.on_render(screen,"Dist : {} cm ".format(self.dist),'top','left')
    def on_event(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                self.on_start_stop_usdist()
            
    def on_cleanup(self):
        self._usdist = False

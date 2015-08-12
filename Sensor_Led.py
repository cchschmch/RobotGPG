import pygame
from pygame.locals import *
import gopigo
from gopigo import *

class Sensor_Led:
    def __init__(self):
        self._led_left = False
        self._led_right = False
        self.left = 1
        self.right = 0
        print "Sensor_Led :key K L \n"
    def on_init(self):
        self.on_cleanup()
        
    def on_start_stop_led(self,blr,lr):
        blr = not blr
        if blr:
            led_on(lr)
        else:
            led_off(lr)
        return blr
            
    def on_start_stop_led_left(self):
        self._led_left = self.on_start_stop_led(self._led_left,self.left)
            
    def on_start_stop_led_right(self):
        self._led_right = self.on_start_stop_led(self._led_right,self.right)
            
    def on_loop(self):
        pass     
    def on_render(self,screen,drawtext):
        drawtext.on_render(screen,"Led ({},{})".format(self._led_left,self._led_right ),'middle','right')

    def on_event(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k:
                self.on_start_stop_led_left()
            if event.key == pygame.K_l:
                self.on_start_stop_led_right()
            
            
    def on_cleanup(self):
        self._led_left = True
        self._led_right = True
        self.on_start_stop_led_left()
        self.on_start_stop_led_right()

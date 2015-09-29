import pygame
from pygame.locals import *

from Rocket_original import *

class Sensor_Rocket:
    def __init__(self):
        self._delay = 85
        self.rocket_pilot = False
        print "Sensor_Rocket :key R W A S D\n"
    def on_init(self):
        init_rocket()
	
    
    def switchrocket(self):
        self.rocket_pilot = not self.rocket_pilot
        if self.rocket_pilot:
            start_rocket()
            pygame.key.set_repeat(10,10)
        else:
            stop_rocket()
            pygame.key.set_repeat()
    def on_loop(self):
        pass

    def on_render(self,screen,drawtext):
        pass    
    def on_event(self,event):
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.switchrocket()
            if self.rocket_pilot :
                if event.key == pygame.K_a:
                    run_command("left", self._delay)
                elif event.key == pygame.K_d:
                    run_command("right", self._delay)
                if event.key == pygame.K_w:
                    run_command("up", self._delay)
                elif event.key == pygame.K_s:
                    run_command("down", self._delay)
    
    def on_cleanup(self):
        self.rocket_pilot = False
        stop_rocket()
 

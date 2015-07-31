import pygame
import pygame.camera
import os
import time


from Sensor_camera import *
from Sensor_UltraSound import *
from Servo_Util import *
from Sensor_Encoder import *
from DrawText import *
from pygame.locals import *
from Sensor_Led import *
from Sensor_motor import *





class App:
    def __init__(self, width=640, height=400, fps=30):
        self._running = True


        self._display_surf = None
        
        self.width  = width
        self.height = height
        
        self.height_screen = 0
        self.width_screen = 0
        self.size = self.width, self.height
        self.fps = fps
        self.playtime = 0.0
        self.servo_util = Servo_Util()
        self.sensor_camera = Sensor_Camera(width/2,height/2)
        self.sensor_ultrasound = Sensor_UltraSound()
        self.sensor_encoder = Sensor_Encoder()
        self.sensor_led = Sensor_Led()
        self.sensor_motor = Sensor_motor()
        self.drawtext = DrawText(width,height)
        
    def on_init(self):
        pygame.init()
        infoObject = pygame.display.Info()
        self.width_screen = infoObject.current_w
        self.height_screen = infoObject.current_h

        
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self._running = True
        self.sensor_camera.on_init()
        self.sensor_ultrasound.on_init()
        self.drawtext.on_init()
        self.servo_util.on_init()
        self.sensor_encoder.on_init()
        self.sensor_led.on_init()
        self.sensor_motor.on_init()

    def on_event_key(self,event):
    	if event.key == pygame.K_ESCAPE:
            self._running = False

    def on_event_mouse(self,down,event):
        pass
    
    def on_event(self, event):
        self.sensor_camera.on_event(event,self.screen)
        self.sensor_ultrasound.on_event(event)
        self.servo_util.on_event(event)
        self.sensor_encoder.on_event(event)
        self.sensor_led.on_event(event)
        self.sensor_motor.on_event(event)
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            self.on_event_key(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.on_event_mouse(True,event)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.on_event_mouse(False,event)

    



    def on_loop(self):
        self.miliseconds = self.clock.tick(self.fps)
        self.playtime+=self.miliseconds / 1000.0
        self.sensor_camera.on_loop()
        self.servo_util.on_loop()
        self.sensor_ultrasound.on_loop()
        self.sensor_encoder.on_loop()
        self.sensor_led.on_loop()
        self.sensor_motor.on_loop()
    
    def on_render(self):
        self.screen.blit(self.background, (0,0))
        self.sensor_camera.on_render( self.screen)
        self.sensor_ultrasound.on_render(self.screen,self.drawtext)
        self.drawtext.on_render(self.screen,"FPS : {:6.3} {} PLAYTIME: {:6.3} Seconds".format(self.clock.get_fps(), " "*5, self.playtime),'bottom')
        self.servo_util.on_render(self.screen,self.drawtext)
        self.sensor_encoder.on_render(self.screen,self.drawtext)
        self.sensor_led.on_render(self.screen,self.drawtext)
        self.sensor_motor.on_render(self.screen,self.drawtext)
        pygame.display.flip()
        
    def on_cleanup(self):
        self.sensor_camera.on_cleanup()
        self.sensor_ultrasound.on_cleanup()
        self.servo_util.on_cleanup()
        self.drawtext.on_cleanup()
        self.sensor_encoder.on_cleanup()
        self.sensor_led.on_cleanup()
        self.sensor_motor.on_cleanup()
        pygame.quit()
        
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

 
if __name__ == "__main__" :
    
    
    theApp = App(640,400,15)
    theApp.on_execute()


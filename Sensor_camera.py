import pygame
import pygame.camera

from pygame.locals import *

class Sensor_Camera:
    def __init__(self, width=640, height=400):
        self._camera = False
        self.width  = width
        self.height = height
        self.size = self.width, self.height
        
    def on_init(self):        
        pygame.camera.init()
        self.camera = pygame.camera.Camera("/dev/video0",(self.size))

    def on_camera(self,screen):
        if not self._camera:
            self.camera.start()
            self.camera.set_controls(hflip = True, vflip = True)
            self.snapshot = pygame.surface.Surface((self.size),0,screen)
        else:
            self.camera.stop()
        self._camera = not self._camera
        
    def off_camera(self):
        if self._camera:         
            self.camera.stop()
        self._camera = not self._camera
        
    def on_loop(self):
        if self._camera:
            if self.camera.query_image():
                self.snapshot = self.camera.get_image(self.snapshot)
                
    def on_event(self,event,screen):
        if event.type == pygame.KEYDOWN:        
            if event.key == pygame.K_c:
                self.on_camera(screen)
                
    def on_render(self,screen):
        if self._camera:
            screen.blit(self.snapshot, (0,0))

    def on_cleanup(self):
        if self._camera:
            self.off_camera()

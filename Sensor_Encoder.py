import pygame
from pygame.locals import *
import gopigo

from gopigo import *

class Sensor_Encoder:
    def __init__(self):
        self._encoder = False
        self.m1 = 0
        self.m2 = 0
        self.target = 0
        self.do_encoder = False
        self.read_encoder = ''
        print "Sensor_Encoder :key E\n"
    def on_init(self):
        print ("Voltage GoPiGo : %f \n",volt())
       pass
    
    def on_start_stop_encoder(self):
        self._encoder = not self._encoder
        if self._encoder:
            enable_encoders()
        else:
            disable_encoders()
            
    def set_encoder_parameters(self,m1,m2,target):
        self.m1 = m1
        self.m2 = m2
        self.target = target
        self.do_encoder = True
        
    def on_loop(self):
        if self._encoder:
            self.read_encoder = read_enc_status()
            if self.do_encoder:
                enc_tgt(self.m1,self.m2,self.target)
                self.do_encoder = False
                
    def on_render(self,screen,drawtext):
        if self._encoder:
            drawtext.on_render(screen,"Encoder : {} {} {} : {}".format(self.m1,self.m2,self.target,self.read_encoder),'middle','left')

    def on_event(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                self.on_start_stop_encoder()
            
    def on_cleanup(self):
        self._encoder = False
        disable_encoders()

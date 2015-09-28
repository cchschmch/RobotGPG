import pygame
import gopigo


from pygame.locals import *


class Servo_Util:
    def __init__(self):
        self._servo = False
        self.old_servo_pos = 90
        self.servo_pos = 90
        self.servo_step_angle = 10
        print "Servo_Util :key o <- -> up down space\n"
    def on_init(self):
        pass
    def on_start_stop_servo(self):
        if not self._servo:
            gopigo.enable_servo()    
        else:
            gopigo.disable_servo()
        self._servo = not self._servo
        
       
    def on_right_servo(self):
        if self._servo:
            self.servo_pos=self.servo_pos+self.servo_step_angle
            if self.servo_pos>180:
                self.servo_pos = 180
                
    def on_left_servo(self):
        if self._servo:
            self.servo_pos=self.servo_pos-self.servo_step_angle
            if self.servo_pos<0:
                 self.servo_pos = 0
    def on_increase_servo(self):
        if self._servo:
            self.servo_step_angle = self.servo_step_angle+1
            if self.servo_step_angle>30:
                self.servo_step_angle = 30
    def on_decrease_servo(self):
        if self._servo:
            self.servo_step_angle = self.servo_step_angle-1
            if self.servo_step_angle<1:
                self.servo_step_angle = 1
    def on_reset_servo(self):
        if self._servo:
            self.servo_pos=90
            
    def on_loop(self):
        if self._servo:
            if self.servo_pos!=self.old_servo_pos:
                gopigo.servo(self.servo_pos)
                self.old_servo_pos = self.servo_pos
                pygame.time.delay(50)
                
    def on_event(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_o:
               self.on_start_stop_servo()
            elif event.key == pygame.K_LEFT:
               self.on_left_servo() 
            elif event.key == pygame.K_RIGHT:
               self.on_right_servo()
            elif event.key == pygame.K_UP:
               self.on_increase_servo() 
            elif event.key == pygame.K_DOWN:
               self.on_decrease_servo()    
            elif event.key == pygame.K_SPACE:
               self.on_reset_servo()
           
    def on_render(self,screen,drawtext):
        if self._servo:
            drawtext.on_render(screen,"At {} deg {}".format(self.old_servo_pos,self.servo_step_angle),'top','right')
        
    def on_cleanup(self):
        if self._servo:
            self.on_start_stop_servo()
            

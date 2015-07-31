import pygame
from pygame.locals import *
import gopigo
from gopigo import *

class Sensor_Motor:
    def __init__(self):
        self._motor_left = 200
        self._motor_right = 200
        self._motor_dual = 200
        self._motor_step = 10
        self.dualmotors = False
        self.leftmotor = False
        self.rightmotor = False
    def on_init(self):
        pass
        
    def switchdualmotors():
        self.dualmotors = not self.dualmotors
        if self.dualmotors:
            self.leftmotor = False
            self.rightmotor = False

    def switchleftmotor():
        self.leftmotor = not self.leftmotor
        if self.leftmotor:
            self.dualmotors = False
    

    def switchrightmotor():
        self.rightmotor = not self.rightmotor
        if self.rightmotor:
            self.dualmotors = False


    def UPMotorSpeed():
        if self.dualmotors:
            self._motor_dual = self._motor_dual +self._motor_step
        else:
            if self.leftmotor:
                self._motor_left = self._motor_left+self._motor_step
            if self.rightmotor:
                self._motor_right = self._motor_right+self._motor_step


    def DOWBMotorSpeed():
        if self.dualmotors:
            self._motor_dual = self._motor_dual -self._motor_step
        else:
            if self.leftmotor:
                self._motor_left = self._motor_left-self._motor_step
            if self.rightmotor:
                self._motor_right = self._motor_right-self._motor_step

    def on_loop(self):
        if self.dualmotors:
            set_speed(self._motor_dual)
        else:
            if self.leftmotor:
                set_left_speed(self._motor_left)
            if self.rightmotor:
                set_right_speed(self._motor_right)

    def on_render(self,screen,drawtext):
        motor = ""
        speed =""
        if self.dualmotors:
            motor = "Dual "
            speed = "{} ".format(self._motor_dual)
        else:
            if self.leftmotor:
                motor = "Left "
                speed = "{} ".format(self._motor_left)
            if self.rightmotor:
                motor = motor + "Right"
                speed = speed + "{}".format(self._motor_right)

        drawtext.on_render(screen,"Motor {} at speed {}".format(motor,speed),'middle','right')
    
    def on_event(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                self.switchdualmotors()
            if event.key == pygame.K_PLUS:
                self.UPMotorSpeed()
            if event.key == pygame.K_MINUS:
                self.DOWNMotorSpeed()
            if event.key == pygame.K_v:
                self.switchleftmotor()
            if event.key == pygame.K_v:
                self.switchrightmotor()
    
    def on_cleanup(self):
        self.dualmotors = False
        self.leftmotor = False
        self.rightmotor = False

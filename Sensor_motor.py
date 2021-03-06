import pygame
from pygame.locals import *
import gopigo
from gopigo import *
from Sensor_Led import *

class Sensor_Motor:
    def __init__(self):
        self._motor_left = 200
        self._motor_right = 200
        self._motor_dual = 200
        self._motor_step = 10
        self.dualmotors = False
        self.leftmotor = False
        self.rightmotor = False
        self.LedSensor=None


    def on_init(self):
        print "Sensor_Motor :key V B N = -  \n"
        print "             i\n"
        print "          j     k\n"
        print"              m\n"
        print "   1 : stop\n"

    def SetLedSensor(self,LedSensor):
        self.LedSensor=LedSensor
        print "synchro Led with left roght motor\n"
    def switchdualmotors(self):
        self.dualmotors = not self.dualmotors
        if self.dualmotors:
            self.leftmotor = False
            self.rightmotor = False

    def switchleftmotor(self):
        self.leftmotor = not self.leftmotor
        if self.leftmotor:
            self.dualmotors = False
    

    def switchrightmotor(self):
        self.rightmotor = not self.rightmotor
        if self.rightmotor:
            self.dualmotors = False

    def setMotorSpeed(self,dual):
        self._motor_dual =  dual
    def UPMotorSpeed(self):
        if self.dualmotors:
            self._motor_dual = self._motor_dual +self._motor_step
            if self._motor_dual>255:
                self._motor_dual=255
        else:
            if self.leftmotor:
                self._motor_left = self._motor_left+self._motor_step
                if self._motor_left>255:
                    self._motor_left=255

            if self.rightmotor:
                self._motor_right = self._motor_right+self._motor_step
                if self._motor_right>255:
                    self._motor_right=255


    def DOWNMotorSpeed(self):
        if self.dualmotors:
            self._motor_dual = self._motor_dual -self._motor_step
            if self._motor_dual<0:
                self._motor_dual = 0
        else:
            if self.leftmotor:
                self._motor_left = self._motor_left-self._motor_step
                if self._motor_left<0:
                    self._motor_left = 0
            if self.rightmotor:
                self._motor_right = self._motor_right-self._motor_step
                if self._motor_right<0:
                    self._motor_right = 0
                    
    def forward(self):
	self.stop()
        fwd()
        if self.LedSensor is not None:
                self.LedSensor.on_start_led_left()
		self.LedSensor.on_start_led_right()

    def backward(self):
        self.stop()
	bwd()
    def left(self):
	self.stop()
        left_rot()
	if self.LedSensor is not None:
		self.LedSensor.on_start_led_left()
    def right(self):
	self.stop()
        right_rot()
        if self.LedSensor is not None:
                self.LedSensor.on_start_led_right()

    def stop(self):
        stop()
        if self.LedSensor is not None:
                self.LedSensor.on_stop_leds()

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
        if motor != "":
            drawtext.on_render(screen,"Motor {} at speed {}".format(motor,speed),'middle','left')
    
    def on_event(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                self.switchdualmotors()
            if event.key == pygame.K_EQUALS:
                self.UPMotorSpeed()
            if event.key == pygame.K_MINUS:
                self.DOWNMotorSpeed()
            if event.key == pygame.K_v:
                self.switchleftmotor()
            if event.key == pygame.K_n:
                self.switchrightmotor()
            if event.key == pygame.K_i:
                self.forward()
            if event.key == pygame.K_m:
                self.backward()
            if event.key == pygame.K_j:
                self.left()
            if event.key == pygame.K_k:
                self.right()
            if event.key == pygame.K_1:
                self.stop()
    def on_cleanup(self):
        self.dualmotors = False
        self.leftmotor = False
        self.rightmotor = False

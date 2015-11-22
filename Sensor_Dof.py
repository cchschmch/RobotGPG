import sys, getopt

sys.path.append('.')
import RTIMU
import os.path
import time
import math
import pygame
from pygame.locals import *


class Sensor_Dof:
    def __init__(self):
        self._dof = False
        self._dof_init = False
        self.angle = 0
        self.poll_interval = 1
        print "Sensor_Dof :key f\n"
        self.SETTINGS_FILE = "RTIMULib"

        print("Using settings file " + self.SETTINGS_FILE + ".ini")
        if not os.path.exists(self.SETTINGS_FILE + ".ini"):
            print("Settings file does not exist, will be created")

        self.settings = RTIMU.Settings(self.SETTINGS_FILE)
        self.imu = RTIMU.RTIMU(self.settings)

        print("IMU Name: " + self.imu.IMUName())

        if (not self.imu.IMUInit()):
            print("IMU Init Failed")  
        else:
            print("IMU Init Succeeded")
            self._dof_init = True
        
    def on_init(self):
        # this is a good time to set any fusion parameters
        if self._dof_init:
            self.imu.setSlerpPower(0.02)
            self.imu.setGyroEnable(True)
            self.imu.setAccelEnable(True)
            self.imu.setCompassEnable(True)

            self.poll_interval = self.imu.IMUGetPollInterval()
            print("Recommended Poll Interval: %dmS\n" % self.poll_interval)

    def on_start_stop_dof(self):
        if self._dof_init:
            self._dof = not self._dof
            
    def get_data(self):
        if self.imu.IMURead():
            test =0
            while (test<20):
                data = self.imu.getIMUData()
                fusionPose = data["fusionPose"]
                self.angle = math.degrees(fusionPose[2])
                time.sleep(self.poll_interval*1.0/1000.0)
        return self.angle
    
    def on_loop(self):
        if self._dof_init:
            if self._dof:
                self.get_data()
                
    def on_render(self,screen,drawtext):
        if self._dof_init:
            if self._dof:
                drawtext.on_render(screen,"Angle : " + str(self.angle),'top','middle')
    def on_event(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                self.on_start_stop_dof()
            
    def on_cleanup(self):
        self._dof = False

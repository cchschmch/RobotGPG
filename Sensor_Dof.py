import sys, getopt
import threading

sys.path.append('.')
import RTIMU
import os.path
import time
import math
import pygame
from pygame.locals import *


class Sensor_Dof_Thread (threading.Thread):
    def __init__(self,sensor_dof):
        sensor_dof.angle = 0
        self.poll_interval = 1
        print "Sensor_Dof :key f\n"
        self.SETTINGS_FILE = "RTIMULib"
        self.sensor_dof = sensor_dof
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
            sensor_dof._dof_init = True

        # this is a good time to set any fusion parameters
        if sensor_dof._dof_init:
            self.imu.setSlerpPower(0.02)
            self.imu.setGyroEnable(False)
            self.imu.setAccelEnable(False)
            self.imu.setCompassEnable(True)

            self.poll_interval = self.imu.IMUGetPollInterval()
            print("Recommended Poll Interval: %dmS\n" % self.poll_interval)
            threading.Thread.__init__(self)
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def get_data(self):
        if self.imu.IMURead():
            data = self.imu.getIMUData()
            fusionPose = data["fusionPose"]
            self.sensor_dof.angle = math.degrees(fusionPose[2])
            time.sleep(self.poll_interval*1.0/1000.0)
    def run(self):
        while self.sensor_dof._dof_init:
            self.get_data()

class Sensor_Dof:
    def __init__(self):
        self._dof = False
        self._dof_init = False

    def on_init(self):
        self.sdt = Sensor_Dof_Thread(self)
        self.sdt.start()

    def on_start_stop_dof(self):
        if self._dof_init:
            self._dof = not self._dof
            

    
    def on_loop(self):
        pass
                
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
        self._dof_init = False
        self.sdt.stop()

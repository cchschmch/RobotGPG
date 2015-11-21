import sys, getopt
import gopigo
import RTIMU
import os.path
import math

from GPG_Pos_Dist import*
from random import randint
from time import sleep

from gopigo import *
from Sensor_Dof import *
from Sensor_Motor import *



class main_usd_sample:
    num_version = 1
    delay =0.2
    lim=250
    def acquire_usd(self,num_sample):
        all_sample=[]
        sumdist = 0
        for test_num_sample in range(num_sample):
            dist = gopigo.us_dist(15)
            all_sample.append(dist)
            if dist<self.lim and dist>=0:
                sumdist=dist+sumdist
            else:
                sumdist=self.lim+sumdist


        dist = 	sumdist/num_sample
        print "acquire usd mid :",dist
        return all_sample

    def rotate_usd(self,servo_pos):
        print "rotate usd ",servo_pos
        gopigo.servo(90+servo_pos)
        sleep(self.delay)
    def current_main(self):
        
        
    def rotate_main(self,sensor_dof,sensor_motor,relative_pos):
        initial_pos = sensor_dof.get_data()
        current_pos = initial_pos
        to_pos = initial_pos+relative_pos
        if to_pos>180:
            to_pos = to_pos-360
        if to_pos<-180
            to_pos=to_pos+360

        sensor_motor.stop()
        test_pos = sensor_dof.get_data()
        if relative_pos>0:
            sensor_motor.right()
        else:
            sensor_motor.left()
        while (abs(test_pos-to_pos)>0.5):
            test_pos = sensor_dof.get_data()
        sensor_motor.stop()
        test_pos = sensor_dof.get_data()
        return test_pos

        

if __name__ == "__main__":
    if len(sys.argv) !=2:
        print 'usage: GenerateSampleGpG.py <path_to_file_to_save> \n You must specify the path to the file you want to save as the first arg'
        sys.exit(1)
    filename = sys.argv[1]
    sensor_dof = Sensor_Dof()
    sensor_dof.on_init()

    sensor_motor = Sensor_Motor()
    sensor_motor.on_init()
    sensor_motor.switchdualmotors()
    sensor_motor.setMotorSpeed(90)
    sensor_motor.on_loop()

    gopigo.enable_servo()
    print "enable_servo"
    sample_acquire = main_usd_sample()
    sample = GPG_Pos_Dist()
    sample.release_element()
    sample_acquire.rotate_usd(0)
    print "Current angle :",sensor_dof.get_data()
    new_angle = sample_acquire.rotate_main(sensor_dof,sensor_motor,30);
    print "New angle :",new_angle
    exit(0);

    one_sample = GPG_Pos_Dist_Element()
    icurrenta = 0
    istepb = 5
    icurrentb = -85
    while icurrentb<86:
        sample_acquire.rotate_usd(icurrentb)
        usd = sample_acquire.acquire_usd(5)
        one_sample.set_all(0,0,icurrenta,icurrentb)
        one_sample.set_all_usd(usd,5)
        sample.add_element(one_sample)
        icurrentb = icurrentb+ istepb
    sample_acquire.rotate_usd(0)
    sample_acquire.rotate_usd(0)
    sample_acquire.rotate_usd(0)

    gopygo_version = fw_ver()
    info = 'Generated by GoPiGo Version : ' + str(gopygo_version) + ' GeneratedSampleGpG.py version :'+str(sample_acquire.num_version)
    io = GPG_Pos_Dist_IO(sample.get_version())
    io.ToFile(sample,filename,info)
    sample_acquire.rotate_usd(0)
    gopigo.disable_servo()
    print "disable_servo"

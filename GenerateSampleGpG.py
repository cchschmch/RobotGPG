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
from Sensor_motor import *



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
        #print "acquire usd mid :",dist
        return all_sample

    def rotate_usd(self,servo_pos):
        #print "rotate usd ",servo_pos
        gopigo.servo(90+servo_pos)
        sleep(self.delay)

    def compute_pos_modulo(self,to_pos):
        if to_pos>180:
            to_pos = to_pos-360
        if to_pos<-180:
            to_pos=to_pos+360
        return to_pos

    def rotate_main(self,sensor_dof,sensor_motor,relative_pos):
        initial_pos = sensor_dof.angle
        current_pos = initial_pos
        to_pos = initial_pos+relative_pos
        to_pos = self.compute_pos_modulo(to_pos)
        num_test = 0
        wait_motor_stop = 0.5
        wait_motor = 0.75

        sensor_motor.stop()
        sleep(wait_motor_stop)
        test_pos = sensor_dof.angle
        dist = to_pos-test_pos


        print "test pos ",test_pos," to_pos ",to_pos, " dist ",dist, " test ",num_test
        if relative_pos>0:
            #print "Goto right"
            sensor_motor.right()
            sleep(wait_motor)
        else:
            #print "Goto left"
            sensor_motor.left()
            sleep(wait_motor)
        ok_turn = True
        while (ok_turn):
            sensor_motor.stop()
            sleep(wait_motor_stop)
            test_pos = sensor_dof.angle
            dist = to_pos-test_pos
            dist = self.compute_pos_modulo(dist)
            num_test = num_test +1
            print "test pos",test_pos," to_pos",to_pos, "dist",dist, " test ",num_test
            if (abs(dist)<0.5):
                ok_turn = False;
            else:
                ok_turn= True;
                if dist>0:
                    #print "Goto right"
                    sensor_motor.right()
                    sleep(wait_motor)
                else:
                    #print "Goto left"
                    sensor_motor.left()
                    sleep(wait_motor)

        sensor_motor.stop()
        test_pos = sensor_dof.angle
        print "Reach pos " , test_pos , " in ", num_test
        return test_pos

    def acquire_cone_usd(self,angle_main,one_sample,istep_usd,icone_usd,max_sample_usd ):
        max_angle_usd = -85
        angle_usd = -icone_usd/2
        if angle_usd<max_angle_usd:
            angle_usd = max_angle_usd
        sample_acquire.rotate_usd(0)
        while angle_usd<=-angle_usd:
            print "usd rotate ",angle_usd
            sample_acquire.rotate_usd(angle_usd)
            usd = sample_acquire.acquire_usd(max_sample_usd)
            one_sample.set_all(0,0,angle_main,angle_usd)
            one_sample.set_all_usd(usd,max_sample_usd)
            sample.add_element(one_sample)
            angle_usd = angle_usd+ istep_usd

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
    print "Current angle :",sensor_dof.angle

    one_sample = GPG_Pos_Dist_Element()
    istep_main = 66
    iangle_main = 0
    istep_usd = 10
    icone_usd = 60
    max_sample_usd = 2
    angle_main = sensor_dof.angle
    sample_acquire.acquire_cone_usd(angle_main,one_sample,istep_usd,icone_usd,max_sample_usd)
    while iangle_main<360-istep_main:
        angle_main = sample_acquire.rotate_main(sensor_dof,sensor_motor,istep_main);
        sample_acquire.rotate_usd(0)
        sample_acquire.rotate_usd(0)
        sample_acquire.rotate_usd(0)
        sample_acquire.acquire_cone_usd(angle_main,one_sample,istep_usd,icone_usd,max_sample_usd)
        iangle_main = iangle_main+istep_main



    sample_acquire.rotate_usd(0)
    sample_acquire.rotate_usd(0)
    sample_acquire.rotate_usd(0)

    print "disable sensor_dof"
    sensor_dof.on_cleanup()

    gopygo_version = fw_ver()
    info = 'Generated by GoPiGo Version : ' + str(gopygo_version) + ' GeneratedSampleGpG.py version :'+str(sample_acquire.num_version)
    io = GPG_Pos_Dist_IO(sample.get_version())
    io.ToFile(sample,filename,info)
    sample_acquire.rotate_usd(0)
    gopigo.disable_servo()
    print "disable_servo"

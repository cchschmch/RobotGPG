import sys
import gopigo
from GPG_Pos_Dist import*
from random import randint
from time import sleep
from gopigo import *

class usd_sample:
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
        print "rotate ",servo_pos
        gopigo.servo(90+servo_pos)
        sleep(self.delay)


if __name__ == "__main__":
    if len(sys.argv) !=2:
        print 'usage: GenerateSampleGpG.py <path_to_file_to_save> \n You must specify the path to the file you want to save as the first arg'
        sys.exit(1)
    filename = sys.argv[1]
    gopigo.enable_servo()
    print "enable_servo"
    sample_acquire = usd_sample()
    sample = GPG_Pos_Dist()
    sample.release_element()
    sample_acquire.rotate_usd(0)
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


import gopigo
from GPG_Pos_Dist import*
from random import randint
from time import sleep

class usd_sample:
    delay =0.2
    lim=250
    def acquire_usd(self,num_sample):
        test_num_sample = 0
        sumdist = 0
        for test_num_sample in range(num_sample):
            dist = gopigo.us_dist(15)
            if dist<self.lim and dist>=0:
                sumdist=dist+sumdist
	    else:
		sumdist=self.lim+sumdist
	dist = 	sumdist/num_sample
        print "acquire usd",dist
        return dist

    def rotate_usd(self,servo_pos):
        print "rotate ",servo_pos
        gopigo.servo(90+servo_pos)
        sleep(self.delay)


if __name__ == "__main__":
    gopigo.enable_servo()
    print "enable_servo"
    sample_acquire = usd_sample()
    sample = GPG_Pos_Dist()
    sample.release_element()
    sample_acquire.rotate_usd(0)
    one_sample = GPG_Pos_Dist_Element()
    icurrenta = 0
    istepb = 1
    icurrentb = -85
    while icurrentb<86:
        sample_acquire.rotate_usd(icurrentb)
        usd = sample_acquire.acquire_usd(5)
        one_sample.set_all(0,0,icurrenta,icurrentb,usd)
        sample.add_element(one_sample)
        icurrentb = icurrentb+ istepb


    io = GPG_Pos_Dist_IO()
    io.ToFile(sample,'sample')
    sample_acquire.rotate_usd(0)
    gopigo.disable_servo()
    print "disable_servo"

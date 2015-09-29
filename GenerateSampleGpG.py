
import gopigo
from GPG_Pos_Dist import*
from random import randint
from time import sleep

class usd_sample:
    def acquire_usd(self):
        sleep(0.205)
        dist1 = gopigo.us_dist(15)
        sleep(0.205)
        dist2 = gopigo.us_dist(15)
        #dist = randint(1, 200)
        dist = (dist1+dist2)/2
        print "acquire usd",dist
        return dist

    def rotate_usd(self,servo_pos):
        print "rotate ",servo_pos
        gopigo.servo(90+servo_pos)


if __name__ == "__main__":
    gopigo.enable_servo()
    print "enable_servo"
    sample_acquire = usd_sample()
    sample = GPG_Pos_Dist()
    sample.release_element()

    one_sample = GPG_Pos_Dist_Element()
    icurrenta = 0
    istepb = 2
    icurrentb = -30
    while icurrentb<31:
        sample_acquire.rotate_usd(icurrentb)
        usd = sample_acquire.acquire_usd()
        one_sample.set_all(0,0,icurrenta,icurrentb,usd)
        sample.add_element(one_sample)
        icurrentb = icurrentb+ istepb


    io = GPG_Pos_Dist_IO()
    io.ToFile(sample,'sample')
    gopigo.disable_servo()
    print "disable_servo"
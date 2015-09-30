
import gopigo
from GPG_Pos_Dist import*
from random import randint
from time import sleep

class usd_sample:
    def acquire_usd(self):
        sleep(500/1000)
        dist1 = gopigo.us_dist(15)
        sleep(500/1000)
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
    
    sample_acquire.rotate_usd(0)
    
    sample_acquire.rotate_usd(0)
    gopigo.disable_servo()
    print "disable_servo"

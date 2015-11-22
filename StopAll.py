import sys, getopt
import gopigo


from GPG_Pos_Dist import*


from gopigo import *
from Sensor_motor import *

sensor_motor = Sensor_Motor()
sensor_motor.on_init()
sensor_motor.stop()
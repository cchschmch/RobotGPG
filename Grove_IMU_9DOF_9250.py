#!/usr/bin/env python

import smbus
import time
import math
import RPi.GPIO as GPIO
import struct

rev = GPIO.RPI_REVISION
if rev == 2 or rev == 3:
    bus = smbus.SMBus(1)
else:
    bus = smbus.SMBus(0)


IMU_9DOF_9250 = 0x68

MODE_REGISTER =0x02

#Magnetometer Registers
MPU9150_RA_MAG_ADDRESS=0x0C
MPU9150_RA_MAG_XOUT_L=0x03
MPU9150_RA_MAG_XOUT_H=0x04
MPU9150_RA_MAG_YOUT_L=0x05
MPU9150_RA_MAG_YOUT_H=0x06
MPU9150_RA_MAG_ZOUT_L=0x07
MPU9150_RA_MAG_ZOUT_H=0x08
MPU9250_CLOCK_PLL_XGYRO =       0x01
MPU9250_CLOCK_PLL_YGYRO =       0x02
MPU9250_CLOCK_PLL_ZGYRO =       0x03

MPU9250_GYRO_FS_250     =   0x00
MPU9250_GYRO_FS_500     =   0x01
MPU9250_GYRO_FS_1000    =   0x02
MPU9250_GYRO_FS_2000    =   0x03


MPU9250_ACCEL_FS_2      =   0x00
MPU9250_ACCEL_FS_4      =   0x01
MPU9250_ACCEL_FS_8      =   0x02
MPU9250_ACCEL_FS_16     =   0x03


MPU9250_RA_ACCEL_XOUT_H  =  0x3B
MPU9250_RA_ACCEL_XOUT_L  =  0x3C
MPU9250_RA_ACCEL_YOUT_H  =  0x3D
MPU9250_RA_ACCEL_YOUT_L  =  0x3E
MPU9250_RA_ACCEL_ZOUT_H  =  0x3F
MPU9250_RA_ACCEL_ZOUT_L  =  0x40
MPU9250_RA_INT_PIN_CFG   =  0x37


MPU9250_RA_PWR_MGMT_1     = 0x6B

MPU9250_PWR1_CLKSEL_BIT   =     2
MPU9250_PWR1_CLKSEL_LENGTH=     3

MPU9250_RA_CONFIG         =  0x1A
MPU9250_RA_GYRO_CONFIG    =  0x1B
MPU9250_RA_ACCEL_CONFIG   =  0x1C
MPU9250_GCONFIG_FS_SEL_BIT    =  4
MPU9250_GCONFIG_FS_SEL_LENGTH =  2
MPU9250_ACONFIG_AFS_SEL_BIT      =   4
MPU9250_ACONFIG_AFS_SEL_LENGTH   =   2
MPU9250_PWR1_SLEEP_BIT     =     6

def twos_comp(val, bits):
    """compute the 2's compliment of int value val"""
    if( (val&(1<<(bits-1))) != 0 ):
        val = val - (1<<bits)
    return val


class compass_9DOF:
    #accell
        ax=0
        ay=0
        az=0
        #gravity
        gx=0
        gy=0
        gz=0
        #magnetic
        mx=0
        my=0
        mz=0
        
        heading=0
        headingDegrees=0

        def setClockSource(self,  source):
            bus.write_byte_data(IMU_9DOF_9250, MPU9250_RA_PWR_MGMT_1, MPU9250_PWR1_CLKSEL_BIT, MPU9250_PWR1_CLKSEL_LENGTH, source);

        def setFullScaleGyroRange(self,  range):
            bus.write_byte_data(IMU_9DOF_9250, MPU9250_RA_GYRO_CONFIG, MPU9250_GCONFIG_FS_SEL_BIT, MPU9250_GCONFIG_FS_SEL_LENGTH, range);

        def setFullScaleAccelRange(self, range):
            bus.write_byte_data(IMU_9DOF_9250, MPU9250_RA_ACCEL_CONFIG, MPU9250_ACONFIG_AFS_SEL_BIT, MPU9250_ACONFIG_AFS_SEL_LENGTH, range);

        def setSleepEnabled(self,  enabled) :
            bus.write_byte_data(IMU_9DOF_9250, MPU9250_RA_PWR_MGMT_1, MPU9250_PWR1_SLEEP_BIT, enabled);

        def __init__(self):
            self.setClockSource(MPU9250_CLOCK_PLL_XGYRO)
            self.setFullScaleGyroRange(MPU9250_GYRO_FS_250)
            self.setFullScaleAccelRange(MPU9250_ACCEL_FS_2)
            self.setSleepEnabled(False)
            
            
            #Enable the compass
            bus.write_byte_data(IMU_9DOF_9250,MODE_REGISTER,0)
            time.sleep(.1)
            data=bus.read_i2c_block_data(IMU_9DOF_9250,0)
                #compass.update(self)
    


        def UpdateGravityAccell(self):
            data=bus.read_i2c_block_data(MPU9150_RA_MAG_ADDRESS,MPU9250_RA_ACCEL_XOUT_H)
            #  *ax = (((int16_t)buffer[0]) << 8) | buffer[1];
            #  *ay = (((int16_t)buffer[2]) << 8) | buffer[3];
            #  *az = (((int16_t)buffer[4]) << 8) | buffer[5];
            #  *gx = (((int16_t)buffer[8]) << 8) | buffer[9];
            #  *gy = (((int16_t)buffer[10]) << 8) | buffer[11];
            #  *gz = (((int16_t)buffer[12]) << 8) | buffer[13];
        
        def UpdateMagneto(self):
            bus.write_byte_data(MPU9250_RA_INT_PIN_CFG,MODE_REGISTER,0)
            time.sleep(.1)
            bus.write_byte_data(MPU9150_RA_MAG_ADDRESS,0x0A, 0x01)
            time.sleep(.1)
            data=bus.read_i2c_block_data(MPU9150_RA_MAG_ADDRESS,MPU9150_RA_MAG_XOUT_L)
                #	*mx = (((int16_t)buffer[1]) << 8) | buffer[0];
                #   *my = (((int16_t)buffer[3]) << 8) | buffer[2];
                #   *mz = (((int16_t)buffer[5]) << 8) | buffer[4];
            
            
            self.mx=twos_comp(data[3]*256+data[4],16)
            self.mz=twos_comp(data[5]*256+data[6],16)
            self.my=twos_comp(data[7]*256+data[8],16)
            self.heading=math.atan2(self.my, self.mx)
            if self.heading <0:
                self.heading+=2*math.pi
            if self.heading >2*math.pi:
                self.heading-=2*math.pi
                
            self.headingDegrees=round(math.degrees(self.heading),2)

if __name__ == "__main__":
    c =  compass_9DOF()
    while (1):
        c.UpdateMagneto();
        print ('mx = '+str(c.mx)+' my = '+str(c.my)+' mz = '+str(c.mz))

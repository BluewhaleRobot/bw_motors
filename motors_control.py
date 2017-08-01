#!/usr/bin/env python
#coding:utf-8
import time
import rospy
import os
import serial
import time
from bw_motors.msg import *
h=None
device_port=None

def openDevice():
    global h,device_port
    try:
        print "Opening BlueWhale motors device"
        h = serial.Serial(
            port=device_port,
            baudrate=115200,     # baudrate
            bytesize=8,             # number of databits
            parity=serial.PARITY_EVEN,
            stopbits=1,
            xonxoff=0,              # don't enable software flow control
            rtscts=0,               # don't enable RTS/CTS flow control
            timeout=5               # set a timeout value, None for waiting forever
        )
        print "openDevice success!"
        print "stopping motors!"
        cmd_str = bytearray([0xcd,0xeb,0xd7,0x09,0x74,0x53,0x53,0x53,0x53,0x00,0x00,0x00,0x00])
        h.write(cmd_str)
    except IOError, ex:
        print ex

def callback(data):
    global h
    ma_speed=data.mA_speed
    mb_speed=data.mB_speed
    cmd_str = bytearray([0xcd,0xeb,0xd7,0x09,0x74,0x53,0x53,0x53,0x53,0x00,0x00,0x00,0x00])
    #第一个右轮电机
    if mb_speed>0:
        cmd_str[5+0]=0x46 #F 前进
        cmd_str[9+0]=mb_speed
    elif mb_speed<0:
        cmd_str[5+0]=0x42 #B 后退
        cmd_str[9+0]=-mb_speed
    else:
        cmd_str[5+0]=0x53 #S 停止
        cmd_str[9+0]=0x00
    #第二个右轮电机
    if ma_speed>0:
        cmd_str[5+1]=0x46 #F 前进
        cmd_str[9+1]=ma_speed
    elif ma_speed<0:
        cmd_str[5+1]=0x42 #B 后退
        cmd_str[9+1]=-ma_speed
    else:
        cmd_str[5+1]=0x53 #S 停止
        cmd_str[9+1]=0x00
    #debug only
    #print "recive orders"+str(cmd_str)
    if h != None:
        h.write(cmd_str)

def init():
    global device_port
    rospy.init_node("bw_motors", anonymous=True)
    device_port = rospy.get_param("~port", '/dev/stm32Motor')
    openDevice()
    rospy.Subscriber("bw_motors/cmd",Motors, callback)

if __name__ == "__main__":
    init()
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        rate.sleep()
    if h!=None:
        print "stopping motors!"
        cmd_str = bytearray([0xcd,0xeb,0xd7,0x09,0x74,0x53,0x53,0x53,0x53,0x00,0x00,0x00,0x00])
        h.write(cmd_str)
        h.close()

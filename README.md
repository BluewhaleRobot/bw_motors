# bw_motors
BlueWhale motorKit Ros driver  package

## input topic
      name                                  type        
    /bw_motors/cmd                        bw_motors/Motors      

## input param   
       name                            default
    port                             /dev/stm32Motor

## default serial params
    port                             /dev/stm32Motor
    baud                               115200
    bytesize                              8
    stopbits                              1

## Usage:
### download to xiaoqiang ros workspace
```
cd ~/Documents/ros/src
git clone https://github.com/BlueWhaleRobot/bw_motors.git
cd ..
catkin_make
```
### Quickstart
```
#launch the node,stm32Motor can be change to any ttyUSB device
rosrun bw_motors motors_control.py  _port:=/dev/stm32Motor

#publish motor speed ,left motor -10 equals ten percentage of maxspeed (backward), right motor 10 equals ten percentage of maxspeed (forward)
rostopic pub bw_motors/cmd bw_motors/Motors '{mA_speed: -10, mB_speed: 10}' -l
```
## Made with :heart: by BlueWhale Tech corp.

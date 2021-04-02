#!/usr/bin/env python

import math
import time
import rospy
import graphic

from geometry_msgs.msg import Twist
from homework.msg import Num

# Input data saving
v_lin = []
w_ang = []
delta_t =[]

# Arrays for plotting
x_crd = [0]
y_crd = [0]
x_prbcrd = [0]
y_prbcrd = [0]
x_imcrd = 0
y_imcrd = 0

# Data for calculations
r = 0.05
L = 0.1
N = 4096
b = 0
wlREAL, wrREAL = 0, 0
wlIMG, wrIMG = 0, 0


# Time counter initialization
start_time = time.time()

def creator(data):
    
    #  Publishing encoders data and position data for debugging
    pub = rospy.Publisher('ashed_chatter', Num, queue_size=10)
    msg = Num()

    print(" "*15)
    msg.header.stamp = rospy.Time.now()

    # Dynamic encoders and position computing
    enc1, enc2, crd1, crd2 = immediate_calculations(v_lin[len(v_lin)-2::], w_ang[len(w_ang)-2::], delta_t[len(delta_t)-2::], wlREAL, wrREAL, x_imcrd, y_imcrd)
    msg.enc1 = enc1*4096
    msg.enc2 = enc2*4096
    msg.position.x = crd1
    msg.position.y = crd2

    # Custom user messages for debugging
    try:
        rospy.loginfo(msg.header.stamp)
        rospy.loginfo(msg.enc1)
        rospy.loginfo(msg.enc2)
        rospy.loginfo(msg.position.x)
        rospy.loginfo(msg.position.y)
        pub.publish(msg.header.stamp, msg.enc1, msg.enc2, msg.position.x, msg.position.y)
    except TypeError: pass

    # Creating arrays for plotting
    v_lin.append(data.linear.x)
    w_ang.append(data.angular.z)
    delta_t.append((time.time() - start_time))

def calculations(V, omega, d_t, wlREAL, wrREAL):

    for i in range (1, len(V)):

        deltatime = d_t[i] - d_t[i-1]

        wlREAL, wrREAL = turtleconversion(omega[i],  V[i], wlREAL, wrREAL, deltatime)
        probablecalc(omega[i],  V[i], wlREAL, wrREAL, deltatime, i)

        VREAL = r/2 * (wlREAL + wrREAL)
        omegaREAL = r/L * (wrREAL - wlREAL)
        tetaREAL = omegaREAL * deltatime

        x_crd.append(x_crd[i-1] + (VREAL * math.cos(tetaREAL) * deltatime))
        y_crd.append(y_crd[i-1] + (VREAL * math.sin(tetaREAL) * deltatime))

def turtleconversion(omega, V, wlREAL, wrREAL, d_t):

    # Computing angular velocity for the each wheel
    b = d_t/(5+d_t)

    w_l = (2 * V - omega * L) / (2 * r)
    w_r = (2 * V + omega * L) / (2 * r)
    wl = (b * wlREAL + (1 - b) * w_l)
    wr = (b * wrREAL + (1 - b) * w_r)

    return wl, wr

def probablecalc(omega, V, wlREAL, wrREAL, deltatime, i):

    # Probable algular velocitity for each wheel - no aperiodic link included
    b = deltatime/(1+deltatime)

    w_l = (2 * V - omega * L) / (2 * r)
    w_r = (2 * V + omega * L) / (2 * r)

    VIMG = r/2 * (w_l + w_r)
    omegaIMG = r/L * (w_l - w_r)

    tetaIMG = omegaIMG * deltatime
    x_prbcrd.append(x_prbcrd[i-1] + (VIMG * math.cos(tetaIMG) * deltatime))
    y_prbcrd.append(y_prbcrd[i-1] + (VIMG * math.sin(tetaIMG) * deltatime))


def immediate_calculations(V, omega, d_t, wlREAL, wrREAL, x_imcrd, y_imcrd):  # Kostyl'
    
    for i in range (1, len(V)):

        deltatime = d_t[i] - d_t[i-1]
        
        wlREAL, wrREAL = turtleconversion(omega[i],  V[i], wlREAL, wrREAL, deltatime)
        
        VREAL = r/2 * (wlREAL + wrREAL)
        omegaREAL = r/L * (wrREAL - wlREAL)
        tetaREAL = omegaREAL * deltatime

        x_imcrd = x_crd[i-1] + (VREAL * math.cos(tetaREAL) * deltatime)
        y_imcrd = y_crd[i-1] + (VREAL * math.sin(tetaREAL) * deltatime)

    return wrREAL, wrREAL, x_imcrd, y_imcrd



def listener():
    
    # Gathering turtlebot data
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('cmd_vel', Twist, creator)
    rospy.spin()


if __name__ == '__main__':
    listener()
    
x_crd =[0]
y_crd =[0]
calculations(v_lin, w_ang, delta_t, wlREAL, wrREAL)
graphic.plotter(x_crd, y_crd, x_prbcrd, y_prbcrd)

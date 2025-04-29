#! usr/bin/env python

import rospy
from ar_week5_test.msg import cubic_traj_params
import os
from random import uniform

# Chage the format of loginfo() to print time in readable format instead of the timestamp
os.environ['ROSCONSOLE_FORMAT'] = '[${time:%Y-%m-%d %H:%M:%S}] ${message}'

# This function declares the node 'points_generator' that is publishing 'points' topic
def generator():
    pub = rospy.Publisher('points', cubic_traj_params, queue_size=10)
    rospy.init_node('points_generator')
    rate = rospy.Rate(0.05)
    while not rospy.is_shutdown():
        # Generate random points
        p0 = uniform(-10.0, 10.0)
        pf = uniform(-10.0, 10.0)
        v0 = uniform(-10.0, 10.0)
        vf = uniform(-10.0, 10.0)
        t0 = 0.0
        tf = uniform(5.0, 10.0)
        rospy.loginfo(f"\ngenerated positions: {round(p0, 2), round(pf, 2)} \ngenerated velocities: {round(v0, 2), round(vf, 2)} \ngenerated times: {round(t0, 2), round(tf, 2)}")

        pub.publish(p0, pf, v0, vf, t0, tf)
        rate.sleep()

if __name__ == '__main__':
    try:
        generator()
    except rospy.ROSInterruptException:
        pass



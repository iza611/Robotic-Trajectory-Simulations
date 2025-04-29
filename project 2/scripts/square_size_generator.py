#! /usr/bin/env python

import rospy
from os import environ
from std_msgs.msg import Float32
from random import uniform

# Change the format of loginfo() to print time in readable format instead of the timestamp
environ['ROSCONSOLE_FORMAT'] = '[${time:%Y-%m-%d %H:%M:%S}] ${message}'

# This function declares the node 'generator' that is publishing topic 'square_size'
def generator():
    rospy.init_node('generator')
    pub = rospy.Publisher('square_size', Float32, queue_size=10)

    # Define rate so that data generation and publication happens every 20 seconds
    rate = rospy.Rate(0.05)
    while not rospy.is_shutdown():
        # Generate random length of the square side
        size = uniform(0.05, 0.20)

        # Log and publish generated information
        pub.publish(size)
        rospy.loginfo(f"{rospy.get_caller_id()} {round(size,3)}x{round(size,3)}")

        # Maintain desired rate
        rate.sleep()

# When the script starts, try running generator() function
# In case there is an exception thrown by rate.sleep(), handle it by catching the rospy.ROSInterruptException exception and pass.
if __name__ == '__main__':
    try:
        generator()
    except rospy.ROSInterruptException:
        pass
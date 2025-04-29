#! usr/bin/env python

import rospy
import os
from std_msgs.msg import Float32
from ar_week5_test.msg import cubic_traj_coeffs

# Chage the format of loginfo() to print time in readable format instead of the timestamp
os.environ['ROSCONSOLE_FORMAT'] = '[${time:%Y-%m-%d %H:%M:%S}] ${message}'

# This function is called once the message is received from the 'coeffs' topic
def callback(data, pubs):
    rospy.loginfo(rospy.get_caller_id() + 
                  f"\n{data}")
    pub1, pub2, pub3 = pubs[0], pubs[1], pubs[2]
    a0, a1, a2, a3, tf = data.a0, data.a1, data.a2, data.a3, data.tf

    # It calculates and publishes pos, vel and acc to pub1, pub2 and pub3 for tf amount of time
    rate = rospy.Rate(10)
    start_time = rospy.Time.now()
    while not rospy.is_shutdown():
        # Get current time relative to starting time start_time
        t = (rospy.Time.now() - start_time).to_sec()
        # Control to not exceed the max time tf
        if t >= tf:
            break
        # Calculate position, velocity and acceleration at time t
        pd = a0 + a1*t + a2*t**2 + a3*t**3
        vd = a1 + 2*a2*t + 3*a3*t**2
        ad = 2*a2 + 6*a3*t
        # Publish calculated position, velocity and acceleration
        pub1.publish(pd)
        pub2.publish(vd)
        pub3.publish(ad)
        rospy.loginfo(f"[{t}s] Publishing pos:{pd}, vel:{vd}, acc:{ad}")

        rate.sleep()


# This function declares the node 'plotter' that is publishing 'position_trajectory', 
# 'velocity_trajectory' and 'acceleration_trajectory' topics and subscribes to 'coeffs' topic
def plotter():
    rospy.init_node('plotter')
    rospy.loginfo("Ready to plot.")

    pub1 = rospy.Publisher('position_trajectory', Float32, queue_size=10)
    pub2 = rospy.Publisher('velocity_trajectory', Float32, queue_size=10)
    pub3 = rospy.Publisher('acceleration_trajectory', Float32, queue_size=10)

    rospy.Subscriber('coeffs', cubic_traj_coeffs, callback, [pub1, pub2, pub3])

    rospy.spin()

if __name__ == '__main__':
    plotter()
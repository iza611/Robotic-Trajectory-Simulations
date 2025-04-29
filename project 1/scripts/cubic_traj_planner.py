#! usr/bin/env python

import rospy
import os
from ar_week5_test.msg import cubic_traj_params, cubic_traj_coeffs
from ar_week5_test.srv import compute_cubic_traj

# Chage the format of loginfo() to print time in readable format instead of the timestamp
os.environ['ROSCONSOLE_FORMAT'] = '[${time:%Y-%m-%d %H:%M:%S}] ${message}'

# This function is called once the message is received from the 'points' topic
def callback(data, pub):
    rospy.loginfo(rospy.get_caller_id() + 
                  f"\n{data}")
    # It requests to compute coefficients from service 'coeffs_srv' 
    rospy.wait_for_service('coeffs_srv')
    try:
        service1_proxy = rospy.ServiceProxy('coeffs_srv', compute_cubic_traj)
        resp = service1_proxy(data.p0, data.pf, data.v0, 
                              data.vf, data.t0, data.tf)
        rospy.loginfo(f"\n{resp}")
        # Once it gets the response, it publishes the results to the 'coeffs' topic
        pub.publish(resp.a0, resp.a1, resp.a2, resp.a3, data.t0, data.tf)
    except rospy.ServiceException as e:
        rospy.logerr("Service call failed: {}".format(e))

    
# This function declares the node 'planner' that is publishing 'coeffs' topic and subscribes to 'points' topic
def planner():
    rospy.init_node('planner')
    pub = rospy.Publisher('coeffs', cubic_traj_coeffs, queue_size=10)
    rospy.Subscriber('points', cubic_traj_params, callback, pub)
    rospy.spin()

if __name__ == '__main__':
    planner()


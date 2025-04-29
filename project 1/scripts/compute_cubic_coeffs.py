#! usr/bin/env python

import rospy
from ar_week5_test.srv import compute_cubic_traj
import numpy as np

# This function is called when there is a request message to service 'coeffs_srv'
def handle_calculations(req):
    b = np.array([req.p0, req.v0, req.pf, req.vf])
    t0, tf = req.t0, req.tf
    M = np.array([[1, t0, t0**2, t0**3],
                  [0, 1, 2*t0, 3*t0**2],
                  [1, tf, tf**2, tf**3],
                  [0, 1, 2*tf, 3*tf**2]])
    M_inv = np.linalg.inv(M)
    # Compute coefficients with formula a = M⁻¹ • b
    a = np.dot(M_inv, b)
    print(f"Returning coefficients {a}")
    return a[0], a[1], a[2], a[3]

# This function declares the node 'compute_coeffs_server' that advertises the service 'coeffs_srv'
def compute_coeffs_server():
    rospy.init_node('compute_coeffs_server')
    s = rospy.Service('coeffs_srv', compute_cubic_traj, handle_calculations)
    print("Ready to compute coeffs")
    rospy.spin()

if __name__ == '__main__':
    compute_coeffs_server()

#! usr/bin/env python

import rospy
from std_msgs.msg import Float32
from math import pi
import moveit_commander
import sys
from moveit_msgs.msg import DisplayTrajectory 
import copy

# Code for the class MoveGroup is heavily inspired by MoveIt tutorial:
# https://github.com/ros-planning/moveit_tutorials/blob/melodic-devel/doc/move_group_python_interface/scripts/move_group_python_interface_tutorial.py
# The class is using Mouve Group Interface that provides an interface to conduct number of operations on the robot
class MoveGroup(object):
    
    def __init__(self):
        super(MoveGroup, self).__init__()
        
        # Initialise 'moveit_commander' to control and plan robot motions with 'RobotCommander' and 'MoveGroupCommander'
        moveit_commander.roscpp_initialize(sys.argv)
        # Instantiate a 'RobotCommander' object to get information about robot's current state
        robot = moveit_commander.RobotCommander()
        # Instantiate MoveGroupCommander object with the group name 'panda_arm' for motion planing and execution
        move_group = moveit_commander.MoveGroupCommander("panda_arm")

        # Create a publisher 'display_traj_pub' to display trajectories in Rviz
        display_traj_pub = rospy.Publisher("/move_group/display_planned_path", DisplayTrajectory, queue_size=20)

        # Print basic info
        print("============ Available Planning Groups:", robot.get_group_names())
        print("============ Printing robot state")
        print(robot.get_current_state())
        print("")

        # Add variables to the instance of the MoveGroup class, referred to by 'self'.
        self.robot = robot
        self.move_group = move_group
        self.display_traj_pub = display_traj_pub

    # This method is used to move six robot joints to the initial positions: [0, -pi/4, 0, -pi/2, 0, pi/3]
    def go_to_start_conf(self):
        move_group = self.move_group

        # Specify goal postion
        joint_goal = move_group.get_current_joint_values()
        joint_goal[0] = 0
        joint_goal[1] = -pi / 4
        joint_goal[2] = 0
        joint_goal[3] = -pi / 2
        joint_goal[4] = 0
        joint_goal[5] = pi / 3
        joint_goal[6] = 0

        # Move the robot to the values specified by 'joint_goal'
        move_group.go(joint_goal, wait=True)
        # Ensure any residual motion is stopped and target pose is cleared
        move_group.stop() 
        move_group.clear_pose_targets()

    # This method is used to plan the robot movement along a square path based on the given size of the square side 'scale'
    def plan_cartesian_path(self, scale=1):
        move_group = self.move_group

        # Initialise empty list to store the path points and ensure scale is in correct data type
        waypoints = []
        scale = float(scale)

        # Increment the y-position, which represents one side of the square
        wpose = move_group.get_current_pose().pose
        wpose.position.y += scale 
        waypoints.append(copy.deepcopy(wpose))

        # Next, increment the x-position to move robot to the next corner of the square
        wpose.position.x += scale
        waypoints.append(copy.deepcopy(wpose))

        # Reverse the first move in y-position to move to the next corner
        wpose.position.y -= scale 
        waypoints.append(copy.deepcopy(wpose))

        # Finally, move back to the corner that was a starting postion by decrementing x-position  
        wpose.position.x -= scale
        waypoints.append(copy.deepcopy(wpose))

        # Plan a Cartesian path through the waypoints list
        (plan, fraction) = move_group.compute_cartesian_path(waypoints, 0.01, 0.0)

        return plan

    # This method takes a planned path and displays it in Rviz
    def show_planned_trajectory(self, plan):
        robot = self.robot
        display_traj_pub = self.display_traj_pub

        # Create a 'DisplayTrajectory' object and add the planned path to it 
        display_traj = DisplayTrajectory()
        display_traj.trajectory_start = robot.get_current_state()
        display_traj.trajectory.append(plan)

        # Publish the created 'DisplayTrajectory' object to the '/move_group/display_planned_path' topic to visualise it in Rviz
        display_traj_pub.publish(display_traj)

        return display_traj

    # This method is used to execute the planned path
    def execute_plan(self, plan):
        # Wait for the '/move_group/display_planned_path' topic to start publishing
        rospy.wait_for_message('/move_group/display_planned_path', DisplayTrajectory)

        # Get the MoveGroupCommander instance and execute the path using MoveIt
        move_group = self.move_group
        move_group.execute(plan, wait=True)

# This function is called once the message is received from the 'square_size' topic.
# It performs four steps: move to starting position, plan, display, and execute a cartesian path in the shape of a square of the received size. 
def callback(data, move_group_obj):
    print(f"============ Received square size = {data.data} ...")

    print(f"============ Going to the start configuration ...")
    move_group_obj.go_to_start_conf()

    print("============ Planning motion trajectory ...")
    plan = move_group_obj.plan_cartesian_path(data.data)
    rospy.sleep(5)

    print("============ Showing planned trajectory ...")
    move_group_obj.show_planned_trajectory(plan)
    rospy.sleep(5)

    print("============ Executing planned trajectory ...")
    move_group_obj.execute_plan(plan)

    print("==============================================================")
    print("============ Waiting for desired size of square trajectory ...")

# This function declares the node 'mover' that is subscribing to 'square_size' topic
# It also creates the object instance of a MoveGroup class and passes it to the callback function
def mover():
    try:
        print("============ Initializing ...")
        move_group_obj = MoveGroup()
        rospy.init_node('mover')

        print("============ Waiting for desired size of square trajectory ...")
        rospy.Subscriber('square_size', Float32, callback, move_group_obj)
        rospy.spin()

    except rospy.ROSInterruptException:
        pass
    except KeyboardInterrupt:
        pass

# When the script starts, mover() function is called
if __name__ == '__main__':
    mover()
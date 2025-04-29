Steps to run the package:
0) Follow the instructions on http://docs.ros.org/en/melodic/api/moveit_tutorials/html/doc/getting_started/getting_started.html to download the required packages 'moveit_tutorials' and 'panda_moveit_config'.
1) Download 'project 1' and/or 'project 2'
2) Place the folder 'project 1' / 'project 2' inside directory ~/your_ws/src (replace 'your_ws' with desired catkin workspace)
3) Open a terminal and run command:  cd ~/your_ws/  
4) Run command:  catkin_make
5) Once completed, run command:  roscore
6) Open new terminal window

for the project 1:
7) Run command: roslaunch ar_week5_test cubic_traj_gen.launch
8) Open new terminal window
9) Run command: rosrun rqt_graph rqt_graph
10) You might need to refresh the rqt_graph to see all the nodes and topics

for the project 2:
7) Run command: roslaunch panda_moveit_config demo.launch
8) Open new terminal window
9) Run command: rosrun ar_week10_test square_size_generator.py
10) Open new terminal window
11) Run command: rosrun ar_week10_test move_panda_square.py
12) Open new terminal window
13) Run command: rosrun rqt_plot rqt_plot
14) Add the topics /joint_states/position[i], replacing i with numbers 0, 1, 2, 3, 4, 5 and 6.
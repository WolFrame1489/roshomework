# roshomework
This was created as a simple program, that would simulate the behaviour of a Turtlebot3 with a differential drive. It listens the data from turtlebot, simulates the control system and drives of the robot, and then plots 2 trajectories: real and ideal one.
Works with ROS1 and Ubuntu Noetic
To launch:
1. source all ros files and devel/setup.bash
2. start Turtlebot teleoperation with $ export TURTLEBOT3_MODEL=waffle; roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch
3. start calculation with $ rosrun homework calc.py
4. Drive turtlebot with wasd
5. Stop turtlebot and calc with ctrl+c
6. You will see plot in package file

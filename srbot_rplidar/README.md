NOTE: I just made some small change to make it compatible with ROS 2 Humble
Hawksbill, Ubuntu 22.04 and Raspberry Pi 4. tested only with Rplidar A1

RPLIDAR ROS package
=====================================================================

ROS node and test application for RPLIDAR

Visit following Website for more details about RPLIDAR:

rplidar roswiki: http://wiki.ros.org/rplidar

rplidar HomePage:   http://www.slamtec.com/en/Lidar

rplidar SDK: https://github.com/Slamtec/rplidar_sdk

rplidar Tutorial:  https://github.com/robopeak/srbot_rplidar/wiki

How to build rplidar ros package
=====================================================================

1) Clone this project to your colcon workspace src folder
2) Install Eloquent ROS2 and colcon compiler.


```
cd [your-ros-package-directory]/src

git clone git@github.com:babakhani/srbot_rplidar2.git

cd [your-ros-package-directory]

colcon build --symlink-install

source ./install/setup.bash
```

Check if package exist

```
ros2 pkg list | grep rplidar
```

I. Run rplidar node and view in the rviz
------------------------------------------------------------

```
ros2 launch srbot_rplidar view_rplidar.launch.py
```
# srbot_rplidar2

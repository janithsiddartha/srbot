from launch import LaunchDescription
from launch.actions import ExecuteProcess
import time

def generate_launch_description():
    # Create a list to hold all the launch actions
    ld = LaunchDescription()

    # Add the first command: docker run -it --rm -v /dev:/dev --privileged --net=host microros/micro-ros-agent:humble serial --dev /dev/ttyACM0 -b 115200
    # docker_1_command = ExecuteProcess(
    #     cmd=['docker', 'run', '-it', '--rm', '-v', '/dev:/dev', '--privileged', '--net=host', 'microros/micro-ros-agent:humble', 'serial', '--dev', '/dev/ttyACM0', '-b', '115200']
    # )
    # ld.add_action(docker_1_command)

    # Add the second command: ros2 launch srbot_rplidar rplidar.launch.py
    # rplidar_command = ExecuteProcess(
    #     cmd=['ros2', 'launch', 'srbot_rplidar', 'rplidar.launch.py']
    # )
    # ld.add_action(rplidar_command)

    robot_state_command = ExecuteProcess(
        cmd=['ros2', 'launch', 'srbot_desc', 'robot_state_publisher.launch.py'],
        output='screen'
    )
    ld.add_action(robot_state_command)

    # Add the third command: ros2 run srbot_nodes inverse_kinematics
    ros2_command = ExecuteProcess(
        cmd=['ros2', 'run', 'srbot_nodes', 'inverse_kinematics']
    )
    ld.add_action(ros2_command)

    # Add the fourth command: ros2 run srbot_nodes forward_kinematics
    ros2_command = ExecuteProcess(
        cmd=['ros2', 'run', 'srbot_nodes', 'forward_kinematics']
    )
    ld.add_action(ros2_command)

    ros2_command = ExecuteProcess(
        cmd=['ros2', 'run', 'srbot_nodes', 'test_odom']
    )
    ld.add_action(ros2_command)



    return ld

if __name__ == '__main__':
    generate_launch_description()
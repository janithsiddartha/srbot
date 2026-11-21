from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    # Create a list to hold all the launch actions
    ld = LaunchDescription()

    # Add the first command: ros2 run srbot_nodes converstor
    convertor_node = Node(
        package='srbot_nodes',
        executable='speed_convertor'
    )
    ld.add_action(convertor_node)

    # Add the second command: ros2 run srbot_nodes odom
    odom_node = Node(
        package='srbot_nodes',
        executable='odom'
    )
    ld.add_action(odom_node)

    # Add the third command: ros2 launch srbot_rplidar view_rplidar.launch.py
    view_rplidar_node = ExecuteProcess(
        cmd=['ros2', 'launch', 'srbot_rplidar2', 'view_rplidar.launch.py']
    )
    ld.add_action(view_rplidar_node)

    # Add the fourth command: ros2 launch srbot_desc robot.launch.py
    view_robot_node = ExecuteProcess(
        cmd=['ros2', 'launch', 'srbot_desc', 'robot.launch.py']
    )
    ld.add_action(view_robot_node)

    return ld

if __name__ == '__main__':
    generate_launch_description()

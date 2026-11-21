#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from std_msgs.msg import Int32, Int32MultiArray
from geometry_msgs.msg import TransformStamped
import tf2_ros
from math import pi, cos, sin

class EncoderToOdomNode(Node):

    def __init__(self):
        super().__init__('encoder_to_odom_node')
        self.subscription = self.create_subscription(
            Int32MultiArray, 'encoder_ticks', self.encoder_callback, 10)
        self.odom_publisher = self.create_publisher(Odometry, 'odom', 10)
        self.tf_broadcaster = tf2_ros.TransformBroadcaster(self)

        self.left_ticks_prev = 0
        self.right_ticks_prev = 0
        self.back_ticks_prev = 0
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        # Create a timer for publishing tf at a faster rate
        self.tf_timer = self.create_timer(0.01, self.tf_callback)  # Adjust the frequency as desired (e.g., 100 Hz)

    def encoder_callback(self, msg):
        # Get encoder ticks for current iteration
        left_ticks_curr = msg.data[0]
        right_ticks_curr = msg.data[1]
        back_ticks_curr = msg.data[2]

        # Convert ticks to position (assuming wheel radius = 0.1 and wheelbase = 0.5)
        dt = 0.02  # 20ms or 50 Hz
        wheel_radius = 0.04  # 4cm diameter
        wheelbase = 0.1  # distance between centre of robot and the wheel
        left_counts_per_rev = 670
        right_counts_per_rev = 670
        back_counts_per_rev = 1236

        # Define the angles of the three wheels in radians
        left_wheel_angle = 30 * (pi / 180)
        right_wheel_angle = 150 * (pi / 180)
        back_wheel_angle = 270 * (pi / 180)

        # Calculate wheel distances
        left_distance = (left_ticks_curr - self.left_ticks_prev) * (2 * pi * wheel_radius) / left_counts_per_rev
        right_distance = (right_ticks_curr - self.right_ticks_prev) * (2 * pi * wheel_radius) / right_counts_per_rev
        back_distance = (back_ticks_curr - self.back_ticks_prev) * (2 * pi * wheel_radius) / back_counts_per_rev

        # Calculate delta distances for each wheel
        # Considering global x axis along north direction and global y axis along west direction and global z upwards
        # Also in robot's coordinate frmae, x axis is along forward direction, y axis is along left direction, and z axis is upwards
        delta_x_left = left_distance * cos(pi/6)
        delta_y_left = left_distance * sin(pi/3)

        delta_x_right = right_distance * cos(pi/6)
        delta_y_right = right_distance * sin(pi/3)

        delta_x_back = 0.0
        # delta_x_back = back_distance * cos(back_wheel_angle)
        # delta_y_back = back_distance * sin(back_wheel_angle)
        delta_y_back = back_distance

        # Calculate total delta distances
        delta_x = ( delta_x_left - delta_x_right + delta_x_back ) / 3  # delta_x_back will always be ZERO
        delta_y = ( - delta_y_left - delta_y_right + delta_y_back ) / 3

        # Calculate delta theta using differential drive kinematics
        delta_theta = (1 / 3 * wheelbase) * ( left_distance + right_distance + back_distance ) # might need modification

        # Perform pose estimation
        self.x += delta_x * cos(self.theta) + delta_y * sin(self.theta)
        self.y += delta_y * cos(self.theta) - delta_x * sin(self.theta)
        self.theta += delta_theta

        # Update previous ticks
        self.left_ticks_prev = left_ticks_curr
        self.right_ticks_prev = right_ticks_curr
        self.back_ticks_prev = back_ticks_curr


        # Publish odometry message
        odom = Odometry()
        odom.header.stamp = self.get_clock().now().to_msg()
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_footprint'
        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.position.z = 0.0
        odom.pose.pose.orientation.z = sin(self.theta / 2)
        odom.pose.pose.orientation.w = cos(self.theta / 2)

        # Set the covariance matrix for pose estimation
        # Assuming a simple diagonal covariance matrix for simplicity
        # Adjust the values according to your requirements
        odom.pose.covariance[0] = 0.1  # x
        odom.pose.covariance[7] = 0.1  # y
        odom.pose.covariance[14] = 0.1  # z
        odom.pose.covariance[21] = 0.05  # rotation x
        odom.pose.covariance[28] = 0.05  # rotation y
        odom.pose.covariance[35] = 0.05  # rotation z

        # Set the twist with covariance
        # Assuming zero covariance for simplicity
        # Adjust the values according to your requirements
        odom.twist.twist.linear.x = delta_x / dt  # Linear velocity in x direction
        odom.twist.twist.linear.y = delta_y / dt  # Linear velocity in y direction
        odom.twist.twist.angular.z = delta_theta / dt  # Angular velocity in z direction

        # Set the covariance matrix for twist estimation
        # Assuming a simple diagonal covariance matrix for simplicity
        # Adjust the values according to your requirements
        odom.twist.covariance[0] = 0.1  # linear x
        odom.twist.covariance[7] = 0.1  # linear y
        odom.twist.covariance[14] = 0.1  # linear z
        odom.twist.covariance[21] = 0.05  # angular x
        odom.twist.covariance[28] = 0.05  # angular y
        odom.twist.covariance[35] = 0.05  # angular z

        self.odom_publisher.publish(odom)

    def tf_callback(self):
        # Publish tf transform between "odom" and "base_footprint"
        transform = TransformStamped()
        transform.header.stamp = self.get_clock().now().to_msg()
        transform.header.frame_id = "odom"
        transform.child_frame_id = "base_footprint"
        transform.transform.translation.x = self.x
        transform.transform.translation.y = self.y
        transform.transform.rotation.z = sin(self.theta / 2)
        transform.transform.rotation.w = cos(self.theta / 2)

        self.tf_broadcaster.sendTransform(transform)

def main(args=None):
    rclpy.init(args=args)
    node = EncoderToOdomNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
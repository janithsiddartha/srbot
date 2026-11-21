#!/usr/bin/env python3

import numpy as np
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32MultiArray
from nav_msgs.msg import Odometry
from std_msgs.msg import Int32, Int32MultiArray
from geometry_msgs.msg import TransformStamped
import tf2_ros
from math import pi, cos, sin

class OdomPublisher(Node):
    
    def __init__(self):
        super().__init__('odom_publisher_')
        self.subscription = self.create_subscription(Int32MultiArray, 'encoder_ticks', self.cmd_vel_callback, 10)
        self.odom_publisher = self.create_publisher(Odometry, 'odom', 10)
        self.tf_broadcaster = tf2_ros.TransformBroadcaster(self)
        self.tf_timer = self.create_timer(0.005, self.tf_callback)  # Adjust the frequency as desired (e.g., 200 Hz)

        self.front_ticks_prev = 0
        self.left_ticks_prev = 0
        self.right_ticks_prev = 0
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        self.theta_b1 = np.pi / 2
        self.theta_b2 = 7 * np.pi / 6
        self.theta_b3 = 11 * np.pi / 6

        self.psi = 0

        self.a1 = 0.03
        self.a2 = 0.03
        self.a3 = 0.03

        self.phi1 = 0
        self.phi2 = 0
        self.phi3 = 0

        self.dy1 = 0.0
        self.dy2 = 0.08
        self.dy3 = -0.08

        self.dx1 = 0.1
        self.dx2 = -0.06
        self.dx3 = -0.06

        self.l = 0.1

        self.J = np.array([[np.cos(self.theta),-np.sin(self.theta),0],[np.sin(self.theta),np.cos(self.theta),0],[0,0,1]])

        self.K1 = np.dot((np.dot([1.0/self.a1,np.tan(self.phi1)*1.0/self.a1],[[np.cos(self.theta_b1),np.sin(self.theta_b1)],[-np.sin(self.theta_b1),np.cos(self.theta_b1)]])),[[1.0,0.0,-self.dy1],[0.0,1.0,self.dx1]])
        self.K2 = np.dot((np.dot([1.0/self.a2,np.tan(self.phi2)*1.0/self.a2],[[np.cos(self.theta_b2),np.sin(self.theta_b2)],[-np.sin(self.theta_b2),np.cos(self.theta_b2)]])),[[1.0,0.0,-self.dy2],[0.0,1.0,self.dx2]])
        self.K3 = np.dot((np.dot([1.0/self.a3,np.tan(self.phi3)*1.0/self.a3],[[np.cos(self.theta_b3),np.sin(self.theta_b3)],[-np.sin(self.theta_b3),np.cos(self.theta_b3)]])),[[1.0,0.0,-self.dy3],[0.0,1.0,self.dx3]])
        self.K=[self.K1,self.K2,self.K3]
        # self.K=[[self.K1],[self.K2],[self.K3]]

        # W is the wheel input matrix/input configuration matrix
        # self.W = np.linalg.inv(self.K)
        self.W = (self.a1/3)*np.array([[0,-np.sqrt(3),np.sqrt(3)],[2,-1,-1],[1/self.l,1/self.l,1/self.l]])

        self.eta_dot = [0.0, 0.0, 0.0]

        self.omega = np.array([[0.0],[0.0],[0.0]])
        self.zeta = np.dot(self.W, self.omega)

    def cmd_vel_callback(self, msg):
        # Get encoder ticks for current iteration
        front_ticks_curr = msg.data[0]
        left_ticks_curr = msg.data[1]
        right_ticks_curr = msg.data[2]

        # Convert ticks to position (assuming wheel radius = 0.1 and wheelbase = 0.5)
        dt = 0.02  # 20ms or 50 Hz
        wheel_radius = 0.04  # 100cm diameter
        front_counts_per_rev = 1236
        left_counts_per_rev = 670
        right_counts_per_rev = 670

        # Angular velocities of each wheel 
        omega_1 = (front_ticks_curr - self.front_ticks_prev) * (2 * pi) / (front_counts_per_rev * dt) # front wheel
        omega_2 = (left_ticks_curr - self.left_ticks_prev) * (2 * pi) / (left_counts_per_rev * dt) # left wheel
        omega_3 = (right_ticks_curr - self.right_ticks_prev) * (2 * pi) / (right_counts_per_rev * dt) # right wheel
        self.omega = np.array([[omega_1],[omega_2],[omega_3]])

        # Jacobian matrix J is given by:
        self.J = np.array([[np.cos(self.theta),-np.sin(self.theta),0],[np.sin(self.theta),np.cos(self.theta),0],[0,0,1]])
        # Where [theta] is the orientation of body frame w.r.t. global inertial frame

        # Velocity vector in body frame
        self.zeta = np.dot(self.W, self.omega)

        # eta_dot is the velocity vector with respect to the inertial frame.
        self.eta_dot = np.dot(self.J, self.zeta)

        # Pose of the robot
        self.x += self.eta_dot[0][0] * dt
        self.y += self.eta_dot[1][0] * dt
        self.theta += self.eta_dot[2][0] * dt

        # Update previous ticks
        self.front_ticks_prev = front_ticks_curr
        self.left_ticks_prev = left_ticks_curr
        self.right_ticks_prev = right_ticks_curr

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
        odom.twist.twist.linear.x = self.zeta[0][0]  # Linear velocity in x direction
        odom.twist.twist.linear.y = self.zeta[1][0]  # Linear velocity in y direction
        odom.twist.twist.angular.z = self.zeta[2][0]  # Angular velocity in z direction

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
    odom_publisher_ = OdomPublisher()
    rclpy.spin(odom_publisher_)
    odom_publisher_.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
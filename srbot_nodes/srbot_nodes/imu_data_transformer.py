#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray

class imuToOdomNode(Node):

    def __init__(self):
        super().__init__('imu_to_odom_node')
        self.subscription=self.create_subscription(Float32MultiArray,'imu_publisher',self.imu_callback,10)
        self.odom_publisher=self.create_publisher(Float32MultiArray,'imu',10)

        self.prev_accelerometer = [0.0, 0.0, 0.0]
        self.prev_gyroscope = [0.0, 0.0, 0.0]

        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

    def imu_callback(self,msg):
        # Get encoder ticks for current iteration
        accelerometer=[msg.data[0],msg.data[1],msg.data[2]]
        gyroscope=[msg.data[3],msg.data[4],msg.data[5]]

        dt = 0.1 # 100ms or 10Hz

        delta_x = ( accelerometer[0] - self.prev_accelerometer[0] ) * dt * dt
        delta_y = ( accelerometer[1] - self.prev_accelerometer[1] ) * dt * dt
        delta_theta = ( gyroscope[2]- self.prev_gyroscope[2] ) * dt # change in orientation of the robot

        # Perform pose estimation
        self.x = self.x + delta_x
        self.y = self.y + delta_y
        self.theta = self.theta + delta_theta

        # Update previous ticks
        self.prev_accelerometer = accelerometer
        self.prev_gyroscope = gyroscope

        odom = [self.x, self.y, self.theta]

        odom_msg = Float32MultiArray()
        odom_msg.data = odom  # odom is a list containing [self.x, self.y, self.theta]
        self.odom_publisher.publish(odom_msg)


def main(args=None):
    rclpy.init(args=args)
    node = imuToOdomNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
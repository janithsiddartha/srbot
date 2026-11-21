#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
import matplotlib.pyplot as plt

class PlotterNode(Node):

    def __init__(self):
        super().__init__('plotter_node')
        self.motor_rps_sub = self.create_subscription(
            Float32MultiArray,
            'motor_rps',
            self.motor_rps_callback,
            10)

        self.motor_rps_values = []

    def motor_rps_callback(self, msg):
        self.motor_rps_values = msg.data
        self.plot_values()

    def plot_values(self):
        plt.plot(self.motor_rps_values, label='Motor RPS')
        plt.legend()
        plt.xlabel('Time')
        plt.ylabel('RPS Value')
        plt.title('Motor RPS vs Measured Motor RPS')
        plt.pause(0.01)
        plt.clf()


def main(args=None):
    rclpy.init(args=args)
    plotter_node = PlotterNode()
    try:
        rclpy.spin(plotter_node)
    except KeyboardInterrupt:
        pass

    plotter_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

#!/usr/bin/env python3

import numpy as np
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32MultiArray

class MotorRpsPublisher(Node):
    
    def __init__(self):
        super().__init__('motor_rps_publisher')
        self.subscription=self.create_subscription(Twist,'cmd_vel',self.cmd_vel_callback,10)
        self.publisher=self.create_publisher(Float32MultiArray,'motor_rps',10)

        self.scaling_factor = 3.5

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

        # self.J=np.array([[np.cos(self.psi),-np.sin(self.psi),0],[np.sin(self.psi),np.cos(self.psi),0],[0,0,1]])
        # self.J_inv=np.linalg.inv(self.J)

        self.K1 = np.dot((np.dot([1.0/self.a1,np.tan(self.phi1)*1.0/self.a1],[[np.cos(self.theta_b1),np.sin(self.theta_b1)],[-np.sin(self.theta_b1),np.cos(self.theta_b1)]])),[[1,0,-self.dy1/1.0],[0,1,self.dx1/1.0]])
        self.K2 = np.dot((np.dot([1.0/self.a2,np.tan(self.phi2)*1.0/self.a2],[[np.cos(self.theta_b2),np.sin(self.theta_b2)],[-np.sin(self.theta_b2),np.cos(self.theta_b2)]])),[[1,0,-self.dy2/1.0],[0,1,self.dx2/1.0]])
        self.K3 = np.dot((np.dot([1.0/self.a3,np.tan(self.phi3)*1.0/self.a3],[[np.cos(self.theta_b3),np.sin(self.theta_b3)],[-np.sin(self.theta_b3),np.cos(self.theta_b3)]])),[[1,0,-self.dy3/1.0],[0,1,self.dx3/1.0]])
        self.K=[self.K1,self.K2,self.K3]

    def cmd_vel_callback(self, msg):
        eta_dot = [msg.linear.x,msg.linear.y,msg.angular.z]
        # omega=np.dot(np.dot(self.K,self.J_inv),self.eta_dot)
        omega = np.dot(self.K,eta_dot)

        front_rps_r = omega[0]/self.scaling_factor
        left_rps_r = omega[1]/self.scaling_factor
        right_rps_r = omega[2]/self.scaling_factor

        motor_rps = Float32MultiArray()
        motor_rps.data = [front_rps_r,left_rps_r,right_rps_r]
        self.publisher.publish(motor_rps)

def main(args=None):
    rclpy.init(args=args)
    motor_rps_publisher = MotorRpsPublisher()
    rclpy.spin(motor_rps_publisher)
    motor_rps_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
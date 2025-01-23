#!/usr/bin/env python3

import time
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty, String
from tello_msgs.msg import TelloStatus
import time

class Automation(Node):

    def __init__(self):
        super().__init__('automation')

        self.publisher_takeoff = self.create_publisher(Empty, 'takeoff', 1)
        self.publisher_land = self.create_publisher(Empty, 'land', 1)

        self.timer = self.create_timer(2.0, self.start_sequence)

        self.manual_speed = 35.0  # cm/s

    def start_sequence(self):
        msg = Twist()
        self.timer.cancel()  
        self.takeoff()  
        time.sleep(2)
        for _ in range(4):  
            self.move_forward(20, msg)  
            time.sleep(5)
            self.turn_right(msg)  
            time.sleep(2)
        self.land()  

    def takeoff(self):
        self.publisher_takeoff.publish(Empty())
        self.get_logger().info("Drone decolando...")

    def land(self):
        self.publisher_land.publish(Empty())
        self.get_logger().info("Drone pousando...")

    def move_forward(self, distance, msg):
        while distance > 0:
            #msg = Twist()
            msg.linear.x = self.manual_speed
            self.get_logger().info("Forward")
            distance -=1

    def turn_right(self, msg):
            #msg = Twist()
            msg.linear.y = self.manual_speed
            self.get_logger().info("Right")

def main(args=None):
    rclpy.init(args=args)
    node = Automation()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

#!/usr/bin/env python3

import time
import rclpy
from std_msgs.msg import Empty
import threading


class land_simu():

    def __init__(self):
        rclpy.init()
        self.node = rclpy.create_node('land_simu')
        self.number_of_drones = 4
        self.pos1 = None

        self.pub_land_1 = self.node.create_publisher(
            Empty, '/simu_tello1/land', 1)
        self.pub_land_2 = self.node.create_publisher(
            Empty, '/simu_tello2/land', 1)
        self.pub_land_3 = self.node.create_publisher(
            Empty, '/simu_tello3/land', 1)
        self.pub_land_4 = self.node.create_publisher(
            Empty, '/simu_tello4/land', 1)

        spin_thread = threading.Thread(target=rclpy.spin, args=(self.node,))
        spin_thread.start()

        time.sleep(0.5)

        self.land_all()

        rclpy.shutdown()

    def publish_once_in_cmd_vel(self, pubid: int, cmd: Empty):
        if pubid == 1:
            pub = self.pub_land_1
        elif pubid == 2:
            pub = self.pub_land_2
        elif pubid == 3:
            pub = self.pub_land_3
        elif pubid == 4:
            pub = self.pub_land_4
        else:
            return

        while True:
            connections = pub.get_subscription_count()
            if connections > 0:
                pub.publish(cmd)
                break
            else:
                time.sleep(0.005)

    def land_all(self):
        cmd = Empty()
        for i in range(1, self.number_of_drones+1):
            self.publish_once_in_cmd_vel(i, cmd)


if __name__ == '__main__':
    land_simu()

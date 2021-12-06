#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
import math

class APF:
    def __init__(self):
        self.ranges = []
        self.pose_x = 0.00
        self.pose_y = 0.00
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.sub = rospy.Subscriber('/scan', LaserScan, self.laser_callback)  # Laser information
        self.sub1 = rospy.Subscriber('/odom', Odometry, self.odom_callback)   # Odometry info that acts as thte GPS coordinates
        rospy.sleep(0.5)
        self.rate = rospy.Rate(10)
        self.final_x = 10
        self.final_y = 10
        self.loop()

    def laser_callback(self, msg): # 
        self.ranges = msg.ranges

    
    def odom_callback(self, msg): # we get the current x and y coordinates of the bot
        self.pose_x = msg.pose.pose.position.x
        self.pose_y = msg.pose.pose.position.y
    
    def loop(self):
        Ka = 1/100
        Kr = 1/100
        Kv = 1/100
        Ro = 0.5
        Po = 0.00
        while not rospy.is_shutdown():
            vel_output = Twist()
            v_att_x = -1*Ka*(self.pose_x - self.final_x)
            v_att_y = -1*Ka*(self.pose_y - self.final_y)
            Po = min(self.ranges)
            angle = self.ranges.index(Po)
            x_or = Po*math.cos(math.radians(angle))
            y_or = Po*math.sin(math.radians(angle))
            if Po <= Ro:
                v_rep_x = -1*Kr*(1-(Po/Ro))*x_or/(Po**3)
                v_rep_y = -1*Kr*(1-(Po/Ro))*y_or/(Po**3)
                v_vir_x = -1*Kv*x_or/(x_or**2 + y_or**2)**1.5
                v_vir_y = -1*Kv*y_or/(x_or**2 + y_or**2)**1.5
            else:
                v_rep_x = 0
                v_rep_y = 0
                v_vir_x = 0
                v_vir_y = 0

            vel_output.linear.x = v_att_x + v_rep_x - v_vir_x
            vel_output.angular.z = v_att_y + v_rep_y - v_vir_y
            self.pub.publish(vel_output)

            self.rate.sleep()

def main():
    rospy.init_node('apf_virtual_obstacle', anonymous=True)
    apf = APF()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
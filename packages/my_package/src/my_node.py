#!/usr/bin/env python

import os
import rospy
from duckietown import DTROS
#from std_msgs.msg import String
from sensor_msgs.msg import CompressedImage
import picamera
import picamera.array
#import cv2_to_compressed_imgmsg
import numpy as np
from cv_bridge import CvBridge

class MyNode(DTROS):

    def __init__(self, node_name):
        # initialize the DTROS parent class
        super(MyNode, self).__init__(node_name=node_name)
        # construct publisher
        self.pub = rospy.Publisher('/duckiemon/camera_node/image/compressed', CompressedImage, queue_size=10)

        
    def run(self):
        # publish message every 1 second
        rate = rospy.Rate(30) # 200Hz
        width = 640
        height = 480
       

        with picamera.PiCamera() as camera:
            camera.resolution = (width, height)

            while not rospy.is_shutdown():
                with picamera.array.PiRGBArray(camera) as output:
                    camera.capture(output, 'bgr')
                    output = output.array
                    #red = output[:,:,0]
                    #output[:,:,0] = output[:,:,2]
                    #output[:,:,2] = red
                    compressed_img_msg = br.cv2_to_compressed_imgmsg(output, dst_format='jpg')
                    rospy.loginfo("Publishing image from Picamera")
                    self.pub.publish(compressed_img_msg)
                    rate.sleep()

if __name__ == '__main__':
    # create the node
    br = CvBridge()
    node = MyNode(node_name='my_node')
    # run node
    node.run()
    # keep spinning
    rospy.spin()
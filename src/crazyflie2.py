import roslib
import rospy
import tf
import crazyflie
import time
import math
from crazyflie_gazebo.srv import TLand

nb =0

def landControl(a):
    global nb
    nb = 1
    return []

if __name__ == '__main__':
    global nb
    rospy.init_node('chase_turtlebot')
    
    
    
    
    cf = crazyflie.Crazyflie("cf1", "/cf1")
    cf.setParam("commander/enHighLevel", 1)
    s = rospy.Service('checkLanded', TLand, landControl)


    listener = tf.TransformListener()
    cf.takeoff(targetHeight = 1.2, duration = 3.0)
    time.sleep(5.0)
    
    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:
            (trans,rot) = listener.lookupTransform('/crazyflie', '/base_link', rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue
        print(trans[0],trans[1])
        angle = tf.transformations.euler_from_quaternion(rot)
        cf.goTo(goal = [trans[0]+0.5*math.cos(angle[2]), trans[1]+0.5*math.sin(angle[2]), 1.2], yaw =0.0, duration = 3.0, relative = False)
        time.sleep(0.5)
        
        if nb == 1:

            cf.goTo(goal = [0, 0, 1.5], yaw =0.0, duration = 3.0, relative = False)
            time.sleep(5.0)
            cf.land(targetHeight = 0.0, duration = 3.0)
            time.sleep(15.0)
            cf.stop()
            break
        else :
            continue
                

	

        rate.sleep()

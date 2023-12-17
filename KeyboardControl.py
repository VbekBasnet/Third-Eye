import cv2
from djitellopy import tello
import KeyPressModule as kp
import time

kp.init()
me = tello.Tello()
me.connect()
print(me.get_battery())

me.streamon()

def getKeyboardInput():
    lr, fb, ud, yv = 0,0,0,0
    speed = 50
    rotate = 100

    if kp.getKey("a"): lr= -speed
    elif kp.getKey("d"): lr= speed

    if kp.getKey("w"): fb = speed
    if kp.getKey("s"): fb = -speed

    if kp.getKey("UP"): ud= speed
    elif kp.getKey("DOWN"): ud= -speed

    if kp.getKey("LEFT"): yv = -rotate
    if kp.getKey("RIGHT"): yv = rotate

    if kp.getKey("SPACE"): me.takeoff(); time.sleep([2])
    if kp.getKey("v"):  me.land()



    return [lr,fb,ud,yv]



while True:


    vals = getKeyboardInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])

    
    cv2.waitKey(1)

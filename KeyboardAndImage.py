from djitellopy import tello
import KeyPressModule as kp
import time
import cv2

kp.init()
me = tello.Tello()
me.connect()
print(me.get_battery())

global img
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

    if kp.getKey("SPACE"): me.takeoff()
    if kp.getKey("v"):  me.land(); time.sleep([2])

    if kp.getKey("z"):
        cv2.imwrite(f'Resources/Images/{time.time()}.jpg', img)
        time.sleep(0.2)



    return [lr,fb,ud,yv]



while True:

    vals = getKeyboardInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])

    img = me.get_frame_read().frame
    img = cv2.resize(img, (360, 240))

    cv2.imshow("Image from Tello", img)
    cv2.waitKey(1)

from djitellopy import tello
from time import sleep
import cv2

me = tello.Tello()
me.connect()
print(me.get_battery())

me.takeoff()


me.send_rc_control(-50, 0, 0, 0)
sleep(1)
me.send_rc_control(0,20,0, 0)
sleep(1)
me.send_rc_control(0, 0, 10, 0)
sleep(1)
me.send_rc_control(0, 0, 0,20)
me.land()

if cv2.waitKey(1) & 0xFF == ord('q'):
    me.land()
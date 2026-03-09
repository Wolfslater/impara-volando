from djitellopy import tello
from time import sleep
from keyboard import is_pressed
import cv2

drone = tello.Tello()
drone.connect()
print(f"{drone.get_battery()}")

'''drone.move_forward(40)
sleep(1.5)
drone.move_back(40)
sleep(1.5)

drone.send_rc_control(20,0,0,0)
sleep(3)
drone.send_rc_control(0,20,0,0)
sleep(3)
drone.send_rc_control(-20,0,0,0)
sleep(3)
drone.send_rc_control(0,-20,0,0)
sleep(3)
drone.land()
'''
move = 20
control = [0,0,0,0]

drone.streamon()
while True:
    if is_pressed("z") and not drone.is_flying: drone.takeoff()
    if is_pressed("x") and drone.is_flying: drone.land()
    if is_pressed("w"): control[1] += 1 
    if is_pressed("s"): control[1] -= 1
    if is_pressed("a"): control[0] -= 1
    if is_pressed("d"): control[0] += 1

    #print(*control)
    drone.send_rc_control(*control)
    if is_pressed(" "): [i for i in control = control[i] = 0]
    img = drone.get_frame_read().frame
    cv2.imshow("prova", img)
    cv2.waitKey(1)

drone.send_rc_control(1,0,0,0)
sleep(3)
drone.send_rc_control(0,0,0,0)
sleep(3)
drone.land()
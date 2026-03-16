from djitellopy import tello
from sys import exit
from keyboard import is_pressed
import cv2

drone = tello.Tello()
drone.connect()
print(f"{drone.get_battery()}")

speed = 50
control = [0,0,0,0]

drone.streamon()
while True:
    control = [0,0,0,0]
    if is_pressed("c"): exit()
    if is_pressed("z") and not drone.is_flying: drone.takeoff()
    if is_pressed("x") and drone.is_flying: drone.land()
    if is_pressed("w"): control[1] = speed
    if is_pressed("s"): control[1] = -speed
    if is_pressed("a"): control[0] = -speed
    if is_pressed("d"): control[0] = speed
    if is_pressed("j"): control[3] = speed
    if is_pressed("l"): control[3] = -speed
    if is_pressed("i"): control[2] = speed
    if is_pressed("k"): control[2] = -speed
    if is_pressed(" "): control = [0,0,0,0]

    #print(*control)
    drone.send_rc_control(*control)
    img = drone.get_frame_read().frame
    cv2.imshow("prova", img)
    cv2.waitKey(1)
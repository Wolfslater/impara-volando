from djitellopy import tello
from time import sleep
from keyboard import is_pressed
import cv2

drone = tello.Tello()
drone.connect()
print(f"{drone.get_battery()}")

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
    elif is_pressed(" "): control = [0,0,0,0]

    #print(*control)
    control = [0,0,0,0]
    drone.send_rc_control(*control)
    img = drone.get_frame_read().frame
    cv2.imshow("prova", img)
    cv2.waitKey(1)
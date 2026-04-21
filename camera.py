from djitellopy import tello
from keyboard import is_pressed
import cv2

drone = tello.Tello()
drone.connect()
print(f"{drone.get_battery()}")

drone.streamon()
while True:
    if is_pressed("z") and not drone.is_flying: drone.takeoff()
    if is_pressed("x") and drone.is_flying: drone.land()
    if is_pressed(" "): drone.send_rc_control(0,0,0,0)
    img = drone.get_frame_read().frame
    cv2.imshow("prova", img)
    cv2.waitKey(1)
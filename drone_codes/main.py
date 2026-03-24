from djitellopy import tello
from time import sleep
from drone_functions import *

drone = tello.Tello()
on = False
control = [0, 0, 0, 0]
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

if __name__ == '__main__':
    connectTello("FB0133")
    drone.connect()
    speed = 50
    i = 0

    while not is_pressed("esc"):
        control = [0, 0, 0, 0]
        
        if is_pressed("z") and not drone.is_flying: drone.takeoff()
        elif is_pressed("x") and drone.is_flying: drone.land()
        if is_pressed("e"):
            try:
                cv2.destroyWindow("Output")
                on = False
            except cv2.error:
                pass
        elif is_pressed("q"): on = True
        if on:
            drone.streamon()
            camera()
        elif on == False:
            drone.streamoff()

        isPressed(speed)

        if is_pressed("+")and speed < 100:
            sleep(0.00001)
            speed += 1
        elif is_pressed("-") and speed > 0:
            sleep(0.00001)
            speed -= 1
        
        drone.send_rc_control(control[0], control[1], control[2], control[3])
        if on:
            img = show_img(speed)
            if is_pressed("space"):
                cv2.imwrite(f"file{i}.jpg", img)
                i += 1
                sleep(0.5)

            cv2.imshow("Output", img)
            cv2.waitKey(1)

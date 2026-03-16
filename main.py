from djitellopy import tello
from sys import exit
from keyboard import is_pressed
import cv2

def draw_speed(img, x, y, speed): #creats a rectangle that shows the drone speed
    if is_pressed("q") and speed < 105: speed += 5
    if is_pressed("e") and speed > -100: speed -= 5
    cv2.rectangle(img, (x, y), (x + 30, y + 100), (255, 255, 0), 3)
    cv2.rectangle(img, (x, y + 100 - speed), (x + 30, y + 100), (25, 255, 0), cv2.FILLED)

def send_control(control):
    if is_pressed("c"): exit()
    if is_pressed("z") and not drone.is_flying: drone.takeoff()
    if is_pressed("x") and drone.is_flying: drone.land()
    if is_pressed("w"): control[1] = speed
    if is_pressed("s"): control[1] = -speed
    if is_pressed("a"): control[0] = -speed
    if is_pressed("d"): control[0] = speed
    if is_pressed("j"): control[3] = -speed
    if is_pressed("l"): control[3] = speed
    if is_pressed("i"): control[2] = speed
    if is_pressed("k"): control[2] = -speed
    if is_pressed(" "): control = [0,0,0,0]
    return control

if __name__ == '__main__':
    drone = tello.Tello()
    drone.connect()
    print(f"{drone.get_battery()}")

    speed = 50
    control = [0,0,0,0]

    drone.streamon()
    while True:
        oldcontrol = control.copy()
        control = [0,0,0,0]
        send_control(control)

        #print(*control)
        if (control!=oldcontrol):
            drone.send_rc_control(*control)
        img = drone.get_frame_read().frame
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cv2.putText(img, f"Battery life: {drone.get_battery()}%",
            (690, 100), cv2.QT_FONT_NORMAL, 1, (50, 240, 255), 2)
        draw_speed(img, 10, 10, speed)
        cv2.imshow("prova", img)
        cv2.waitKey(1)
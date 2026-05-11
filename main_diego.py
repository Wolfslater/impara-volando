from djitellopy import tello
from time import sleep
from sys import exit
import cv2
from cvzone.HandTrackingModule import HandDetector
detector = HandDetector(maxHands=2)
from keyboard import is_pressed

key = 0

def draw_speed(img, x, y, speed): #creats a rectangle that shows the drone speed
    if is_pressed("q") and speed < 100: speed += 1
    if is_pressed("e") and speed > 0: speed -= 1
    cv2.rectangle(img, (x, y), (x + 30, y + 100), (255, 255, 0), 3)
    cv2.rectangle(img, (x, y + 100 - speed), (x + 30, y + 100), (25, 255, 0), cv2.FILLED)
    return speed

def send_control(control):
    global speed
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
    if is_pressed("-"): control = [0,0,0,0]
    return control

if __name__ == '__main__':
    drone = tello.Tello()
    drone.connect()
    print(f"{drone.get_battery()}")

    speed = 50
    key = 0
    control = [0,0,0,0]

    drone.streamon()
    while key!=27:
        oldcontrol = control.copy()
        control = [0,0,0,0]
        control = send_control(control)

        #print(*control)
        if (control!=oldcontrol):
            drone.send_rc_control(control[0], control[1], control[2], control[3])
        img = drone.get_frame_read().frame
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        hands, img = detector.findHands(img, draw=True)
        if hands:
            hand = hands[0]
            x,y,w,h = hand['bbox']
            type = hand['type']
            center = hand['center']
            lmList = hand['lmList']
            fingers = detector.fingersUp(hand)

            if fingers[0] == 1: 
                '''#print("debug", fingers[0], fingers[1])
                drone.send_rc_control(20, 0, 0, 0)
                sleep(1)
                drone.send_rc_control(0, 20, 0, 0)
                sleep(1)
                drone.send_rc_control(-20, 0, 0, 0)
                sleep(1)
                drone.send_rc_control(0, -20, 0, 0)'''
                
            if all(f == 1 for f in fingers) and drone.is_flying:
                print("land")  # drone.land()
                if drone.is_flying: 
                    #print("land")
                    drone.land()
            elif fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                if not drone.is_flying:
                    drone.takeoff() #print("takeoff")
            cv2.rectangle(img, (x - 20, y - 20), (x + w + 20, y + h + 20), (0, 255, 0), 2)
            cv2.putText(img, type, (x - 20, y - 30), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
        cv2.putText(img, f"Battery life: {drone.get_battery()}%",
            (690, 100), cv2.QT_FONT_NORMAL, 1, (50, 240, 255), 2)
        speed = draw_speed(img, 10, 10, speed)
        cv2.imshow("prova", img)
        cv2.waitKey(1)
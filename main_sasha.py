from djitellopy import tello
import cv2
import visione_cam
from time import sleep

drone = tello.Tello()
drone.connect()

print(f"Battery: {drone.get_battery()}%")

drone.streamon()

speed = 30

active = False
flying = False

def send_control(fingers):
    global flying

    control = [0, 0, 0, 0]

    if fingers is None:
        return None

    if fingers == [1,1,1,1,1] and active and not flying:
        drone.takeoff()
        flying = True
        return control
    
    elif fingers == [0,0,0,0,0] and flying:
        drone.land()
        flying = False
        return control

    elif fingers == [0,1,0,0,0]:
        control[1] = speed
        sleep(3)

    elif fingers == [0,1,1,0,0]:
        control[1] = -speed
        sleep(3)

    elif fingers == [1,0,0,0,0]:
        control[0] = -speed
        sleep(3)

    elif fingers == [0,0,0,0,1]:
        control[0] = speed
        sleep(3)

    elif fingers == [1,1,0,0,0]:
        control[2] = speed
        sleep(3)
        
    elif fingers == [0,0,0,1,1]:
        control[2] = -speed
        sleep(3)

    elif fingers == [0,1,1,1,0]:
        control[3] = -speed
        sleep(3)

    elif fingers == [0,1,1,1,1]:
        control[3] = speed
        sleep(3)

    return control

while True:

    frame = drone.get_frame_read().frame

    if frame is None:
        continue

    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    fingers = visione_cam.get_fingers(frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('x') and not active:
        active = True
        print("CONTROLLO ATTIVATO")

    if key == 27:  
        break

    if not active:
        cv2.putText(frame, "PRESS X TO START", (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

        cv2.imshow("DRONE CONTROL", frame)
        continue


    control = send_control(fingers)


    if control is None:
        print("MANO NON RILEVATA")

        if active and flying:
            print("FAILSAFE LAND")
            drone.land()
            flying = False

        cv2.imshow("DRONE CONTROL", frame)
        continue  

    drone.send_rc_control(
        control[0],
        control[1],
        control[2],
        control[3]
    )

    cv2.putText(
        frame,
        f"Battery: {drone.get_battery()}%",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (50, 240, 255),
        2
    )

    cv2.putText(
        frame,
        "ACTIVE" if active else "WAITING X",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0) if active else (0, 0, 255),
        2
    )

    cv2.imshow("DRONE CONTROL", frame)



if flying:
    drone.land()

drone.streamoff()
cv2.destroyAllWindows()
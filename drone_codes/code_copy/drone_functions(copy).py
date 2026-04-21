from os import system
import cv2
from keyboard import is_pressed
from main import drone, control, faceCascade

def connectTello(tellonum): #connects the drone automaticly
    ssid = "TELLO-" + tellonum
    return system(f'''cmd /c "netsh wlan connect name={ssid}"''')

def isPressed(speed):

    if is_pressed("a"): control[0] = -speed
    elif is_pressed("d"): control[0] = speed
    if is_pressed("s"): control[1] = -speed
    elif is_pressed("w"): control[1] = speed
    if is_pressed("k"): control[2] = -speed
    elif is_pressed("i"): control[2] = speed
    if is_pressed("j"): control[3] = -speed
    elif is_pressed("l"): control[3] = speed
    #Controls the drone 3d moving patterns

    return control

def draw_speed(img, x, y, speed): #creats a rectangle that shows the drone speed
    cv2.rectangle(img, (x, y), (x + 30, y + 100), (255, 255, 0), 3)
    cv2.rectangle(img, (x, y + 100 - speed), (x + 30, y + 100), (25, 255, 0), cv2.FILLED)
    
def face_distance(faces, img): 
    if len(faces) > 0:
        x,y,w,h = faces[0]
        cv2.putText(img, str(w*h), (0, 140), cv2.QT_FONT_NORMAL, 1, (70, 240, 255), 2)
        return w * h
    return None
#115k max dist
#30k min dist
def show_img(speed):
    img = drone.get_frame_read().frame
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    faces = faceCascade.detectMultiScale(img)

    cv2.putText(img, f"{drone.get_distance_tof()}CM", (50, 100), cv2.QT_FONT_NORMAL, 1, (70, 240, 255), 2)
    cv2.putText(img, f"Battery life: {drone.get_battery()}%", (690, 100), cv2.QT_FONT_NORMAL, 1, (50, 240, 255), 2)
    distance = face_distance(faces, img)
    control = [0, 0, 0, 0]
    if distance is not None:
        if distance < 30000:
            control[1] = 50
        if distance > 90000:
            control[1] = -50
    for f in faces:
        x, y, w, h = f #x, y axis. width and height
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2) #creats a rectangale arounf face-like things
    draw_speed(img, 10, 10, speed) #functon call-back
    return img
    
def camera():
    if is_pressed("1"): drone.set_video_direction(drone.CAMERA_FORWARD)
    elif is_pressed("2"): drone.set_video_direction(drone.CAMERA_DOWNWARD)

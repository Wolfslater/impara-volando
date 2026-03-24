import cv2
from sys import exit
from keyboard import is_pressed

# Camera state variable (starts as off)
off = True
camera = 0

def face_rec():
    global off, camera  # Use the global camera variable
    
    # Only initialize the camera if we're turning it on
    if not off:
        cap = cv2.VideoCapture(camera)  # Initialize camera at the start
        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

        # Continue processing as long as the camera should be on
        while cv2.waitKey(1) != 27 and not off:
            ret, img = cap.read()
            if not ret:
                print("ERROR")
                break

            if camera == 0:
                img = cv2.flip(img, 1)
            faces = faceCascade.detectMultiScale(img)

            for f in faces:
                x, y, w, h = f
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

            cv2.imshow("video", img)

            # Check for key presses within this loop
            if is_pressed("c"):
                off = True
                cv2.destroyWindow("video")
                cap.release()

            elif is_pressed("0"):
                if camera != 0:  # Check if not already using camera 0
                    camera = 0
                    cap.release()  # Release the current camera before switching
                    cap = cv2.VideoCapture(camera)  # Initialize the new camera

            elif is_pressed("1"):
                if camera != 1:  # Check if not already using camera 1
                    camera = 1
                    cap.release()  # Release the current camera before switching
                    cap = cv2.VideoCapture(camera)  # Initialize the new camera

            if is_pressed("k"):
                cap.release()
                exit()

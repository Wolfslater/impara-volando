import cv2 as cv2
#area minore di 30k drone closer
#drone maggiore di 80k si allontana
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
def detect(faces, img):
        if len(faces) > 0:
            x,y,w,h = faces[0]
            cv2.putText(img, str(w*h), (50, 100), cv2.QT_FONT_NORMAL, 1, (70, 240, 255), 2)
            return w * h
        return None

face = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face.detectMultiScale(gray, 1.1, 8)
    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x + w, y + h), (0, 0, 255), 2)
    detect(faces, frame)
    # Display the resting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break
 
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
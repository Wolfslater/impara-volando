import cv2
from cvzone.HandTrackingModule import HandDetector
detector = HandDetector(maxHands=2)
cap = cv2.VideoCapture(0)
key = 0
while key!=27:
    _, img = cap.read()
    hands, img = detector.findHands(img, draw=False)
    if hands:
        hand = hands[0]
        x,y,w,h = hand['bbox']
        type = hand['type']
        center = hand['center']
        lmList = hand['lmList']
        fingers = detector.fingersUp(hand)
        print(fingers)
    cv2.imshow("CAMERA", img)
    key = cv2.waitKey(1)
cap.release()
cv2.destroyAllWindows()
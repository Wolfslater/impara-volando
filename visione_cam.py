import cv2
from cvzone.HandTrackingModule import HandDetector
detector = HandDetector(maxHands=2)
cap = cv2.VideoCapture(0)
key = 0

while key!=27:
    _, img = cap.read()
    hands, img = detector.findHands(img, draw=True)
    if hands:
        hand = hands[0]
        x,y,w,h = hand['bbox']
        type = hand['type']
        center = hand['center']
        lmList = hand['lmList']
        fingers = detector.fingersUp(hand)
        print(fingers)
        cv2.rectangle(img, (x - 20, y - 20), (x + w + 20, y + h + 20), (0, 255, 0), 2)
        cv2.putText(img, type, (x - 20, y - 30), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

    cv2.imshow("CAMERA", img)
    key = cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()
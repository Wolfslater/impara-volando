import cv2
from cvzone.HandTrackingModule import HandDetector

detector = HandDetector(maxHands=1)


def get_fingers(frame):

    if frame is None:
        return None   
    
    frame = cv2.flip(frame, 1)

    hands, frame = detector.findHands(frame, draw=True)

    if hands:
        hand = hands[0]
        return detector.fingersUp(hand)

    return None       
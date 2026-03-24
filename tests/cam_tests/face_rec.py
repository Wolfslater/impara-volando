from face import face_rec, off
from keyboard import is_pressed

if __name__ == '__main__':
    while True:
        if is_pressed("o"):
            import face
            from time import sleep
            face.off = not face.off
            sleep(0.3)
        face_rec()
        if is_pressed("k") and not face_rec():
            exit()
from keyboard import is_pressed
while True:
    if is_pressed("4"): print("4")
    if is_pressed("2"): print("2")
    if is_pressed("6"): print("6")
    if is_pressed("8"): print("8")
    if is_pressed("right"): print("right")
    if is_pressed("left"): print("left")
    if is_pressed("up"): print("up")
    if is_pressed("down"): print("down")
    if is_pressed("e") or is_pressed("maiusc + e"): print("e")
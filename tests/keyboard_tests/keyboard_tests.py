from keyboard import is_pressed
def keys():
    if is_pressed("4"): print("4")
    if is_pressed("2"): print("2")
    if is_pressed("6"): print("6")
    if is_pressed("8"): print("8")
    if is_pressed("right"): print("right")
    if is_pressed("left"): print("left")
    if is_pressed("up"): print("up")
    if is_pressed("down"): print("down")
    if is_pressed("e") or is_pressed("maiusc + e"): print("e")

def isPressed(speed):
    control = [0, 0, 0, 0] #array of the four rotors speed

    if is_pressed("a"): control[0] = -speed
    elif is_pressed("d"): control[0] = speed
    if is_pressed("s"): control[1] = -speed
    elif is_pressed("w"): control[1] = speed
    if is_pressed("shift + s"): control[2] = -speed
    elif is_pressed("shift + w"): control[2] = speed
    if is_pressed("shift + a"): control[3] = -speed
    elif is_pressed("shift + d"): control[3] = speed
    #makes the drone move based on the correspinding pressed key
    
    return control
def land_takeoff():
    if is_pressed("z"): print("takeoff")
    if is_pressed("x"): print("land")
speed = 50
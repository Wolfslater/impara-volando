from keyboard import is_pressed

def drone_speed(speed): #adjusts the drone speed by +5/ -5
    if is_pressed("+") and speed <= 95:
            speed += 5
    elif is_pressed("-") and speed >= 5:
            speed -= 5

speed = 50
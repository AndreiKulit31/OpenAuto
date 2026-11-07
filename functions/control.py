import sys
import pyautogui as pg

def see():
    return pg.screenshot()

def move_mouse(x_pos=0, y_pos=0):
    pg.move(x_pos, y_pos)

def click(type=0, x_pos=0, y_pos=0):
    if type==0:
        pg.leftClick(x_pos, y_pos)
    elif type==1:
        pg.rightClick(x_pos, y_pos)
    else:
        print("Invalid click!") 

    return True

def keyboard_type(text=""):
    pg.write(text)

    return True

if __name__ == "__main__":
    continue_confirm = input("You have entered debugging for functions. Would you like to continue?")

    match continue_confirm.lower():
        case "y":
            move_mouse(0, 0)
            print("Moved Mouse!")
            click(0, 0, 0)
            print("Clicked!")

            keyboard_type("Hello")
            print("Successfully Typed!")
        case "n":
            print("Bye!")
            sys.exit()



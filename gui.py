from tkinter import *
from gesture_click import set_lclick, set_rclick, mouse_clicks
from sign_to_text import set_hold, sign_to_keyboard
from finger_to_cursor import move_cursor
import sys
import PIL.ImageTk
import PIL.Image
import tkinter.ttk as ttk

root = Tk()

root.title("Accessaibility")
root.geometry("960x540")
button = Button()



root.protocol('WM_DELETE_WINDOW', sys.exit)

# try:
#     image = PhotoImage(file="antpookie.png")
# except Exception as e:
#     print(f"Error loading image: {e}")
#     sys.exit()
# image_label = Label(root, image=image)
image = PIL.ImageTk.PhotoImage(PIL.Image.open("antpookie.png"))

# main screen
def main():
    frame = Frame(root, width=960, height=540)
    frame.place(x=0, y=0)

    # button to go to calibration
    calibrate_button = Button(frame, text="Calibrate Actions", command=calibrate_screen)
    calibrate_button.place(x=10, y=10)

    bg = ttk.Label(root, image=image)
    bg.place(relx=0.5, rely=0.5)
    



# calibration screenfaco
def calibrate_screen():
    frame = Frame(root, width=960, height=540)
    frame.place(x=0, y=0)

    # button to change left click (lip-lip threshold)
    lclick_button = Button(frame, text="Set Left Click Threshold", command=set_lclick)
    lclick_button.place(x=10, y=10)


    # button to change right click (forehead-chin threshold)
    rclick_button = Button(frame, text="Set Right Click Threshold", command=set_rclick)
    rclick_button.place(x=10, y=50)

    # button to toggle hold (for the keyboard)
    toggle_hold_button = Button(frame, text="Toggle Keyboard Key Hold", command=set_hold)
    toggle_hold_button.place(x=10, y=90)

    # button to go back to main
    main_button = Button(frame, text="Return", command=main)
    main_button.place(x=10, y=130)

def start():
    main()
    root.mainloop()
    

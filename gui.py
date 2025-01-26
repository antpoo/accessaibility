from tkinter import *

root = Tk()

root.title("Accessaibility")
root.geometry("960x540")
button = Button()

# delete later 
def set_lclick():
    pass
def set_rclick():
    pass
def toggle_hold():
    pass

# main screen
def main():
    frame = Frame(root, width=960, height=540)
    frame.place(x=0, y=0)

    # button to go to calibration
    calibrate_button = Button(frame, text="Calibrate Actions", command=calibrate_screen)
    calibrate_button.place(x=10, y=10)
    



# calibration screen
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
    toggle_hold_button = Button(frame, text="Toggle Keyboard Key Hold", command=toggle_hold)
    toggle_hold_button.place(x=10, y=90)

    # button to go back to main
    main_button = Button(frame, text="Return", command=main)
    main_button.place(x=10, y=130)


main()
root.mainloop()
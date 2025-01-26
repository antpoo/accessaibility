import cv2 as cv
import threading
import sys
from gesture_click import mouse_clicks
from sign_to_text import sign_to_keyboard
from finger_to_cursor import move_cursor
from gui import start

cap_device = 0
cap = cv.VideoCapture(cap_device)
if not cap.isOpened():
  print("Error: could not open webcam")
  exit()


#while True:
def main_app():
  while True:
    # Camera capture #####################################################
    print("balsck")
    ret, image = cap.read()
    if not ret:
        sys.exit()
    image = cv.flip(image, 1)  # Mirror display

    # Detection implementation #############################################################
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    mouse_clicks(image)
    sign_to_keyboard(image)
    move_cursor(image)
    # starts gui
    
main_thread = threading.Thread(target=main_app)
main_thread.start()

start()
# gui_thread = threading.Thread(target=start)
# gui_thread.start()
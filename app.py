import cv2 as cv
from gesture_click import mouse_clicks
from sign_to_text import sign_to_keyboard
from finger_to_cursor import move_cursor

cap_device = 0
cap = cv.VideoCapture(cap_device)
if not cap.isOpened():
  print("Error: could not open webcam")
  exit()

while True:
    # Camera capture #####################################################
    ret, image = cap.read()
    if not ret:
        break
    image = cv.flip(image, 1)  # Mirror display

    # Detection implementation #############################################################
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    mouse_clicks(image)
    sign_to_keyboard(image)
    move_cursor(image)
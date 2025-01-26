import cv2 as cv
from gesture_click import mouse_clicks
from sign_to_text import sign_to_keyboard

cap_device = 0
cap = cv.VideoCapture(cap_device)
if not cap.isOpened():
  print("Error: could not open webcam")
  exit()

while True:
    # Camera capture #####################################################
    cv.waitKey(200)
    ret, image = cap.read()
    if not ret:
        break
    # image = cv.flip(image, 1)  # Mirror display

    # Detection implementation #############################################################
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    mouse_clicks(image)
    sign_to_keyboard(image)

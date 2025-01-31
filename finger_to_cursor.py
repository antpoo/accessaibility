import cv2
import keyboard
import mouse
from constants import *
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.2, min_tracking_confidence=0.2)
mp_drawing = mp.solutions.drawing_utils

# Initialize MediaPipe face
mp_face = mp.solutions.face_mesh
face = mp_face.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils
smoothed_x, smoothed_y = None, None

def move_cursor(rgb_frame: np.ndarray):
    global smoothed_x, smoothed_y
    # Convert the frame to BGR for OpenCV processing
    frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)

    # Process the frame to detect landmarks
    result_hands = hands.process(rgb_frame)

    # Resize the frame to fit the display resolution exactly (stretch)
    frame = cv2.resize(frame, (DISPLAY_WIDTH, DISPLAY_HEIGHT), interpolation=cv2.INTER_LINEAR)

    # Draw the fingertip tracking dot for the right hand only
    if result_hands.multi_hand_landmarks and result_hands.multi_handedness:
        for hand_landmarks, hand_info in zip(result_hands.multi_hand_landmarks, result_hands.multi_handedness):
            if hand_info.classification[0].label == "Right":
                # Extract the tip of the index finger (landmark 8)
                x = hand_landmarks.landmark[8].x * DISPLAY_WIDTH
                y = hand_landmarks.landmark[8].y * DISPLAY_HEIGHT

                # Apply smoothing using exponential moving average
                if smoothed_x is None or smoothed_y is None:
                    smoothed_x, smoothed_y = x, y
                else:
                    smoothed_x = SMOOTHING_FACTOR * smoothed_x + (1 - SMOOTHING_FACTOR) * x
                    smoothed_y = SMOOTHING_FACTOR * smoothed_y + (1 - SMOOTHING_FACTOR) * y
                
                mouse.move(smoothed_x, smoothed_y)

                # Optional: If camera feed should be displayed with landmarks and connections
                cv2.circle(frame, (int(smoothed_x), int(smoothed_y)), 15, (0, 0, 255), -1)
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    
    #######################################################################################
    # result_face = face.process(rgb_frame)
    # if result_face.multi_face_landmarks:
    #     for hand_landmarks in result_face.multi_face_landmarks:
    #         # Index finger tip landmark (Landmark #8 in MediaPipe face)
    #         top_lip = hand_landmarks.landmark[14]
    #         bottom_lip = hand_landmarks.landmark[12]
    #         tl_y = int(top_lip.y * DISPLAY_HEIGHT)
    #         bl_y = int(bottom_lip.y * DISPLAY_HEIGHT)
    #         diff = tl_y-bl_y
    #         if diff>MOUTH_OPEN_THRESHOLD:
    #             mouse.click(button='left')
    ######################################################################################

    # Optional: If camera feed should be displayed
    # cv2.imshow('AccessAIbility', frame)

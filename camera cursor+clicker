import cv2
import keyboard
from screeninfo import get_monitors
import mediapipe as mp
import mouse

# Get display resolution dynamically
monitor = get_monitors()[0]  # Use the primary monitor
DISPLAY_WIDTH = monitor.width
DISPLAY_HEIGHT = monitor.height

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.2, min_tracking_confidence=0.2)
mp_drawing = mp.solutions.drawing_utils

# Initialize MediaPipe face
mp_face = mp.solutions.face_mesh
face = mp_face.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Open the webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not access the webcam.")
    exit()

# Set a keybind to close the program
EXIT_KEY = 'esc'
TILDE_KEY = '`'

SMOOTHING_FACTOR = 0.5  # The closer to 1, the smoother the movement
smoothed_x, smoothed_y = None, None


while True:
    try:
        # Check if the exit key is pressed
        if keyboard.is_pressed(EXIT_KEY):
            print(f"'{EXIT_KEY}' pressed. Exiting...")
            break

        # Check if the tilde key is pressed and perform a left mouse click
        if keyboard.is_pressed(TILDE_KEY):
            mouse.click(button='left')
            print("~",end='')

        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Flip the frame horizontally for a mirror-like effect
        frame = cv2.flip(frame, 1)

        # Convert the frame to RGB for MediaPipe processing
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame to detect landmarks
        result_hands = hands.process(rgb_frame)
        result_face = face.process(rgb_frame)

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

                    # Update mouse position
                    mouse.move(smoothed_x, smoothed_y)

                    # Use smoothed_x and smoothed_y for visualization (red dot and text box)
                    cv2.circle(frame, (int(smoothed_x), int(smoothed_y)), 15, (0, 0, 255), -1)


                    # Optional: Draw hand landmarks and connections
                    #mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        if result_face.multi_face_landmarks:
            for hand_landmarks in result_face.multi_face_landmarks:
                # Index finger tip landmark (Landmark #8 in MediaPipe face)
                top_lip = hand_landmarks.landmark[14]
                bottom_lip = hand_landmarks.landmark[12]
                tl_y = int(top_lip.y * DISPLAY_HEIGHT)
                bl_y = int(bottom_lip.y * DISPLAY_HEIGHT)
                diff = tl_y-bl_y
                if diff>35:
                    mouse.click(button='left')
                # Optional: Draw hand landmarks and connections
                mp_drawing.draw_landmarks(frame, hand_landmarks)

        # Display the frame
        cv2.imshow('AccessAIbility', frame)

        # Exit if 'q' is pressed in the OpenCV window
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    except Exception as e:
        print(f"An error occurred: {e}")
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()

import cv2 as cv
import csv
import copy
import numpy as np
import mediapipe as mp
import itertools
import pydirectinput
from model.keypoint_classifier.keypoint_classifier import KeyPointClassifier
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

def calc_bounding_rect(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_array = np.empty((0, 2), int)

    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)

        landmark_point = [np.array((landmark_x, landmark_y))]

        landmark_array = np.append(landmark_array, landmark_point, axis=0)

    x, y, w, h = cv.boundingRect(landmark_array)

    return [x, y, x + w, y + h]


def calc_landmark_list(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_point = []

    # Keypoint
    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        # landmark_z = landmark.z

        landmark_point.append([landmark_x, landmark_y])

    return landmark_point


def pre_process_landmark(landmark_list):
    temp_landmark_list = copy.deepcopy(landmark_list)

    # Convert to relative coordinates
    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(temp_landmark_list):
        if index == 0:
            base_x, base_y = landmark_point[0], landmark_point[1]

        temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
        temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

    # Convert to a one-dimensional list
    temp_landmark_list = list(itertools.chain.from_iterable(temp_landmark_list))

    # Normalization
    max_value = max(list(map(abs, temp_landmark_list)))

    def normalize_(n):
        return n / max_value

    temp_landmark_list = list(map(normalize_, temp_landmark_list))

    return temp_landmark_list

base_options = python.BaseOptions(model_asset_path='gesture_recognizer.task')
options = vision.GestureRecognizerOptions(base_options=base_options)
recognizer = vision.GestureRecognizer.create_from_options(options)

use_static_image_mode = True
min_detection_confidence = 0.7
min_tracking_confidence = 0.5

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=use_static_image_mode,
    max_num_hands=2,
    min_detection_confidence=min_detection_confidence,
    min_tracking_confidence=min_tracking_confidence,
)

keypoint_classifier = KeyPointClassifier()
with open(
    "model/keypoint_classifier/keypoint_classifier_label.csv", encoding="utf-8-sig"
) as f:
    keypoint_classifier_labels = csv.reader(f)
    keypoint_classifier_labels = [row[0] for row in keypoint_classifier_labels]

cur_char = ''
special_gestures = {"Open_Palm": "capslock", "ILoveYou": "enter", "Thumb_Up": "space", "Thumb_Down": "backspace"}
hold = False
pressed = False

def set_hold(new_hold: bool):
    global hold
    hold = new_hold

def sign_to_keyboard(image: np.ndarray):
    global cur_char, hold, pressed, special_gestures
    debug_image = copy.deepcopy(image)

    image.flags.writeable = False
    results = hands.process(image)
    image.flags.writeable = True

    if results.multi_hand_landmarks is not None:
        for hand_landmarks, handedness in zip(
            results.multi_hand_landmarks, results.multi_handedness
        ):
            if handedness.classification[0].label[0:] == "Right":
                continue
            if isinstance(image, np.ndarray):   
                image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
            recognition_result = recognizer.recognize(image)
            if len(recognition_result.gestures) == 0:
                continue
            new_char = recognition_result.gestures[0][0].category_name

            if not(new_char in special_gestures):
                # Bounding box calculation
                brect = calc_bounding_rect(debug_image, hand_landmarks)
                # Landmark calculation
                landmark_list = calc_landmark_list(debug_image, hand_landmarks)

                # Conversion to relative coordinates / normalized coordinates
                pre_processed_landmark_list = pre_process_landmark(landmark_list)

                # Hand sign classification
                hand_sign_id = keypoint_classifier(pre_processed_landmark_list)

                new_char = keypoint_classifier_labels[hand_sign_id]
            else:
                new_char = special_gestures[new_char]

            new_char = new_char.lower()
            if new_char != cur_char: # new char is shown
                if hold:
                    if cur_char != '' and pressed:
                        print('release', cur_char)
                        pydirectinput.keyUp(cur_char)
                        pressed = False
                    print('press', new_char)
                    pydirectinput.keyDown(new_char)
                    pressed = True
                    print(new_char)
                else:
                    pydirectinput.press(new_char)
                    print(new_char)
                    pressed = False
                cur_char = new_char
                # print(handedness.classification[0].label[0:])
    else: # no more character
        if hold and cur_char != '':
            print('release', cur_char)
            pydirectinput.keyUp(cur_char)
            pressed = False
            cur_char = ''
        cur_char = ''
    
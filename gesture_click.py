# STEP 1: Import the necessary modules.
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import matplotlib.pyplot as plt
import cv2
import mouse

MODEL_PATH = "face_landmarker.task"

left_pressed = False
right_pressed = False

lclick_thresh = 0.1
rclick_thresh = 0.28

ldiff = 0
rdiff = 0

def set_lclick():
  global lclick_thresh, ldiff
  lclick_thresh = ldiff

def set_rclick():
  global rclick_thresh, rdiff
  rclick_thresh = rdiff

BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

def draw_landmarks_on_image(rgb_image, detection_result):

# Debug: Print the number of faces detected
  # if detection_result.face_landmarks:
  #   print(f"Number of faces detected: {len(detection_result.face_landmarks)}")
  # else:
  #   print("No faces detected.")

  face_landmarks_list = detection_result.face_landmarks
  annotated_image = np.copy(rgb_image)

  # Loop through the detected faces to visualize.
  for idx in range(len(face_landmarks_list)):
    face_landmarks = face_landmarks_list[idx]

    # Draw the face landmarks.
    face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    face_landmarks_proto.landmark.extend([
      landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in face_landmarks
    ])

    solutions.drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks_proto,
        connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp.solutions.drawing_styles
        .get_default_face_mesh_tesselation_style())
    solutions.drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks_proto,
        connections=mp.solutions.face_mesh.FACEMESH_CONTOURS,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp.solutions.drawing_styles
        .get_default_face_mesh_contours_style())
    solutions.drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks_proto,
        connections=mp.solutions.face_mesh.FACEMESH_IRISES,
          landmark_drawing_spec=None,
          connection_drawing_spec=mp.solutions.drawing_styles
          .get_default_face_mesh_iris_connections_style())

  return annotated_image


def plot_face_blendshapes_bar_graph(face_blendshapes):
  # Extract the face blendshapes category names and scores.
  face_blendshapes_names = [face_blendshapes_category.category_name for face_blendshapes_category in face_blendshapes]
  face_blendshapes_scores = [face_blendshapes_category.score for face_blendshapes_category in face_blendshapes]
  # The blendshapes are ordered in decreasing score value.
  face_blendshapes_ranks = range(len(face_blendshapes_names))

  fig, ax = plt.subplots(figsize=(12, 12))
  bar = ax.barh(face_blendshapes_ranks, face_blendshapes_scores, label=[str(x) for x in face_blendshapes_ranks])
  ax.set_yticks(face_blendshapes_ranks, face_blendshapes_names)
  ax.invert_yaxis()

  # Label each bar with values
  for score, patch in zip(face_blendshapes_scores, bar.patches):
    plt.text(patch.get_x() + patch.get_width(), patch.get_y(), f"{score:.4f}", va="top")

  ax.set_xlabel('Score')
  ax.set_title("Face Blendshapes")
  plt.tight_layout()
  plt.show()

# STEP 2: Create an FaceLandmarker object.
base_options = python.BaseOptions(model_asset_path='face_landmarker.task')
options = vision.FaceLandmarkerOptions(base_options=base_options,
                                       output_face_blendshapes=True,
                                       output_facial_transformation_matrixes=True,
                                       num_faces=1)
detector = vision.FaceLandmarker.create_from_options(options)

# get face landmarks
def get_landmark_coordinates(detection_result):
  if not detection_result:
    return []
  face_landmarks_list = detection_result.face_landmarks
  all_face_landmarks = []

  for face_landmarks in face_landmarks_list:
    landmarks = [[landmark.x, landmark.y, landmark.z] for landmark in face_landmarks]
    all_face_landmarks.append(landmarks)

  return all_face_landmarks

def mouse_clicks(image: np.ndarray): 
  global left_pressed, right_pressed, lclick_thresh, rclick_thresh, ldiff, rdiff
  # convert to RGB
  rgb_frame = image

  # convert to mediapipe's image format
  mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

  # STEP 4: Detect face landmarks from the input image.
  detection_result = detector.detect(mp_image)

  # STEP 5: Process the detection result. In this case, visualize it.
  annotated_frame = draw_landmarks_on_image(rgb_frame, detection_result)

  # Convert the annotated frame back to BGR for OpenCV
  bgr_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR)

 # Display the frame
  # cv2.imshow("Live Face Landmarks", bgr_frame)

  coords = get_landmark_coordinates(detection_result)

  #print(len(coords))
  
  # if len(coords) > 0:
  #   print(coords[0][15][1], coords[0][19][1])

  if len(coords) > 0:
    upper_lip = coords[0][16][1]
    lower_lip = coords[0][0][1]
    ldiff = upper_lip - lower_lip

    if ldiff >= lclick_thresh and (not left_pressed):

      #print("open")
      mouse.press(button="left")
      left_pressed = True
      
    elif ldiff < lclick_thresh and left_pressed:
      #print("closed")
      mouse.release(button="left")
      left_pressed = False

    forehead = coords[0][10][1]
    #print(forehead)
    chin = coords[0][152][1]
    rdiff = chin - forehead
    if rdiff <= rclick_thresh and (not right_pressed):
      mouse.press(button="right")
      right_pressed = True
    elif right_pressed and rdiff > rclick_thresh:
      mouse.release(button="right")
      right_pressed = False

    left_cheek = coords[0][123][2]
    if left_cheek < 0:
      mouse.wheel(1)
    else:
      mouse.wheel(0)
    # print(left_cheek)

    right_cheek = coords[0][352][2]
    if right_cheek < 0:
      mouse.wheel(-1)
    else:
      mouse.wheel(0)

    nose = coords[0][4][1]
    diff = nose - upper_lip
    # print(diff)

    # diff = top_right_eyelid - bottom_right_eyelid
    # #print (diff)

    # if diff <= 0.135:
    #   mouse.press(button="right")
    # else:
    #   mouse.release(button="right")
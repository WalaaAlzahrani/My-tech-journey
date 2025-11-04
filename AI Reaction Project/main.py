import cv2
import mediapipe as mp
import numpy as np
import time
import os

# --- 0. CONSTANTS & THRESHOLDS ---
# Threshold for the smile (distance between mouth corners and eye corners)
SMILE_THRESHOLD = 0.10

# Threshold for eyes closed (distance between upper and lower eyelids).
EYE_CLOSED_THRESHOLD = 0.015

# Threshold for a raised hand (normalized Y-coordinate of the wrist).
RAISED_THRESHOLD = 0.6

# Threshold for hands covering the face (normalized distance between hand center and nose center).
FACE_COVER_THRESHOLD = 0.15

# New Threshold: Normalized Y-coordinate threshold for index finger tip to be considered "raised/near head"
INDEX_FINGER_RAISED_Y_THRESHOLD = 0.4

# Threshold for index finger touching the mouth (normalized distance between fingertip and mouth center).
FINGER_ON_MOUTH_THRESHOLD = 0.05

# --- IMAGE MAPPING ---
# Map the gesture state string (from the logic section) to the filename
MEME_MAPPING = {
    "NEUTRAL 😐": "neutral.jpg",
    "SMILING 😄": "smiling.jpg",
    "CLOSED EYES 😴": "eyes closed.jpg",
    "HANDS UP ✋": "hands up.jpg",
    "FACE COVERED 😭": "hands covering face.jpg",
    "SHUSH / THINKING 🤔": "thinking.jpg",
    "IDEA / EXCITED 💡": "idea excited.jpg",
}

# --- 1. INITIALIZE MEDIAPIPE & LOAD MEMES ---
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
mp_hands = mp.solutions.hands

# Model initialization
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1, min_detection_confidence=0.5, min_tracking_confidence=0.5
)
hands = mp_hands.Hands(
    max_num_hands=2, min_detection_confidence=0.1, min_tracking_confidence=0.1
)

# Webcam initialization
cap = cv2.VideoCapture(0)
window_name = "AI Reaction App - Two Columns"

# Load all images and store them in a dictionary
loaded_memes = {}
for state, filename in MEME_MAPPING.items():
    try:
        img = cv2.imread(filename)
        if img is None:
            print(
                f"ERROR: Could not load image file: {filename}. Check path and file name."
            )
        loaded_memes[state] = img
    except Exception as e:
        print(f"Error loading {filename}: {e}")

# Check for failed image loads and set a fallback
failed_loads = [img for img in loaded_memes.values() if img is None or img.size == 0]

if failed_loads:
    print(
        "FATAL ERROR: One or more meme images failed to load. Using black screen fallback."
    )
    # Create a simple fallback image (320x240 for a standard 640x480 webcam feed)
    fallback_img = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.putText(
        fallback_img,
        "MEME FAILED",
        (50, 240),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2,
    )

    for state, img in loaded_memes.items():
        if img is None or img.size == 0:
            loaded_memes[state] = fallback_img


# --- 2. LANDMARK INDEXES (Crucial for Logic) ---
LEFT_EYE_TOP = 159
LEFT_EYE_BOTTOM = 145
RIGHT_EYE_TOP = 386
RIGHT_EYE_BOTTOM = 374
LEFT_MOUTH_CORNER = 61
RIGHT_MOUTH_CORNER = 291
NOSE_TIP = 4
WRIST = 0
INDEX_FINGER_TIP = 8
INDEX_FINGER_DIP = 7
MIDDLE_FINGER_TIP = 12
RING_FINGER_TIP = 16
PINKY_FINGER_TIP = 20

# --- 3. CUSTOM DETECTION FUNCTIONS (Same as last working version) ---


def get_landmark_coords(landmarks, index, w, h):
    """Converts normalized landmark coordinates to pixel coordinates."""
    if not landmarks:
        return None
    lm = landmarks[index]
    return int(lm.x * w), int(lm.y * h), lm.x, lm.y


def normalized_distance(p1_x, p1_y, p2_x, p2_y):
    """Calculates the Euclidean distance between two normalized points."""
    return np.sqrt((p1_x - p2_x) ** 2 + (p1_y - p2_y) ** 2)


def is_eyes_closed(face_landmarks, w, h):
    """Detects if the eyes are closed by checking vertical distance between eyelids."""
    if not face_landmarks:
        return False
    left_top_y = face_landmarks[LEFT_EYE_TOP].y
    left_bottom_y = face_landmarks[LEFT_EYE_BOTTOM].y
    right_top_y = face_landmarks[RIGHT_EYE_TOP].y
    right_bottom_y = face_landmarks[RIGHT_EYE_BOTTOM].y
    left_dist = abs(left_top_y - left_bottom_y)
    right_dist = abs(right_top_y - right_bottom_y)
    return (left_dist + right_dist) / 2 < EYE_CLOSED_THRESHOLD


def is_smiling(face_landmarks):
    """Detects a wide smile based on mouth corner-to-mouth corner distance."""
    if not face_landmarks:
        return False
    l_mouth = face_landmarks[LEFT_MOUTH_CORNER]
    r_mouth = face_landmarks[RIGHT_MOUTH_CORNER]
    mouth_width = normalized_distance(l_mouth.x, l_mouth.y, r_mouth.x, r_mouth.y)
    return mouth_width > SMILE_THRESHOLD


def is_hand_raised(hand_landmarks, h):
    """Detects if the hand is in the upper half of the frame."""
    if not hand_landmarks:
        return False
    wrist_y = hand_landmarks[WRIST].y
    return wrist_y < RAISED_THRESHOLD


def is_index_finger_raised_near_head(hand_landmarks_list):
    """Detects if the index finger is explicitly raised (pointing up) near the top of the screen."""
    if not hand_landmarks_list:
        return False
    for hand_landmarks in hand_landmarks_list:
        index_tip_y = hand_landmarks[INDEX_FINGER_TIP].y
        if index_tip_y < INDEX_FINGER_RAISED_Y_THRESHOLD:
            is_index_highest = (
                index_tip_y < hand_landmarks[MIDDLE_FINGER_TIP].y
                and index_tip_y < hand_landmarks[RING_FINGER_TIP].y
                and index_tip_y < hand_landmarks[PINKY_FINGER_TIP].y
            )
            is_index_straight = index_tip_y < hand_landmarks[INDEX_FINGER_DIP].y
            if is_index_highest and is_index_straight:
                return True
    return False


def is_finger_on_mouth(face_landmarks, hand_landmarks_list):
    """Detects if the index finger tip is very close to the mouth/nose area. Used for SHUSH gesture."""
    if not face_landmarks or not hand_landmarks_list:
        return False
    mouth_x = (
        face_landmarks[LEFT_MOUTH_CORNER].x + face_landmarks[RIGHT_MOUTH_CORNER].x
    ) / 2
    mouth_y = (
        face_landmarks[LEFT_MOUTH_CORNER].y + face_landmarks[RIGHT_MOUTH_CORNER].y
    ) / 2
    for hand_landmarks in hand_landmarks_list:
        finger_tip_x = hand_landmarks[INDEX_FINGER_TIP].x
        finger_tip_y = hand_landmarks[INDEX_FINGER_TIP].y
        dist = normalized_distance(mouth_x, mouth_y, finger_tip_x, finger_tip_y)
        if dist < FINGER_ON_MOUTH_THRESHOLD:
            return True
    return False


def is_face_covered(face_landmarks, hand_landmarks_list):
    """Detects if a hand is close to the face center (nose)."""
    if not face_landmarks or not hand_landmarks_list:
        return False
    nose_x = face_landmarks[NOSE_TIP].x
    nose_y = face_landmarks[NOSE_TIP].y
    for hand_landmarks in hand_landmarks_list:
        wrist_x = hand_landmarks[WRIST].x
        wrist_y = hand_landmarks[WRIST].y
        dist = normalized_distance(nose_x, nose_y, wrist_x, wrist_y)
        if dist < FACE_COVER_THRESHOLD:
            return True
    return False


# --- 4. DISPLAY UTILITIES ---


def prepare_display_frames(webcam_frame, current_state, loaded_memes):
    """
    Creates the two frames (live feed and meme feed) and concatenates them.
    """
    H, W, _ = webcam_frame.shape

    # 1. Prepare the Left Frame (Live Feed)
    live_feed = webcam_frame.copy()

    # Add text overlay to the live feed
    cv2.putText(
        live_feed,
        f"Input: {current_state}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0) if current_state != "NEUTRAL 😐" else (255, 255, 255),
        2,
        cv2.LINE_AA,
    )

    # 2. Prepare the Right Frame (Meme Reaction)
    meme_img = loaded_memes.get(current_state)

    # Get the image to display (handling potential failure gracefully)
    if meme_img is None or meme_img.size == 0:
        meme_frame = np.zeros_like(live_feed)
        cv2.putText(
            meme_frame,
            "MEME ERROR",
            (50, H // 2),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2,
        )
    else:
        # Resize the meme to match the height (H) of the webcam feed
        meme_frame = cv2.resize(meme_img, (W, H), interpolation=cv2.INTER_LINEAR)

    # 3. Concatenate the two frames horizontally
    # (Live Feed | Meme Reaction)
    two_column_frame = np.concatenate((live_feed, meme_frame), axis=1)

    return two_column_frame


# --- 5. MAIN LOOP ---
current_state = "NEUTRAL 😐"
last_update_time = time.time()

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    H, W, _ = frame.shape

    # 1. Preprocessing and Model Processing
    frame = cv2.flip(frame, 1)  # Flip for mirror view (User's input)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    rgb_frame.flags.writeable = False

    face_results = face_mesh.process(rgb_frame)
    hand_results = hands.process(rgb_frame)

    # Note: We do NOT draw the landmarks, as we want a clean user input view

    face_landmarks = (
        face_results.multi_face_landmarks[0].landmark
        if face_results.multi_face_landmarks
        else None
    )
    hand_landmarks_list = (
        [h.landmark for h in hand_results.multi_hand_landmarks]
        if hand_results.multi_hand_landmarks
        else []
    )

    # --- 5.1 LOGIC/STATE DETECTION (Priority Order) ---
    new_state = "NEUTRAL 😐"

    if is_face_covered(face_landmarks, hand_landmarks_list):
        new_state = "FACE COVERED 😭"

    elif is_smiling(face_landmarks) and is_index_finger_raised_near_head(
        hand_landmarks_list
    ):
        new_state = "IDEA / EXCITED 💡"

    elif is_finger_on_mouth(face_landmarks, hand_landmarks_list):
        new_state = "SHUSH / THINKING 🤔"

    elif any(is_hand_raised(hlm, H) for hlm in hand_landmarks_list):
        new_state = "HANDS UP ✋"

    elif is_eyes_closed(face_landmarks, W, H):
        new_state = "CLOSED EYES 😴"

    elif is_smiling(face_landmarks):
        new_state = "SMILING 😄"

    # Update state only if it changes or enough time has passed
    if new_state != current_state or (time.time() - last_update_time) > 0.5:
        current_state = new_state
        last_update_time = time.time()

    # --- 5.2 TWO-COLUMN DISPLAY ---

    # Prepare the side-by-side display
    display_frame = prepare_display_frames(frame, current_state, loaded_memes)

    # --- 5.3 DISPLAY & CLEANUP ---
    # Add quit instruction at the bottom of the combined frame
    cv2.putText(
        display_frame,
        "Press 'q' to quit",
        (10, H - 10),  # Positioned in the live feed column
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        1,
        cv2.LINE_AA,
    )

    cv2.imshow(window_name, display_frame)

    if cv2.waitKey(5) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

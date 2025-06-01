import threading
import cv2
import mediapipe as mp
from recognize_speech import recognize_speech
from trigger_command import trigger_command
from commands_enum import COMMANDS

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

prev_x = None
prev_y = None

threshold_x = 100
threshold_y = 100


thread = threading.Thread(target=recognize_speech)
thread.start()

                
def extract_hands_coordinates(hand_landmarks):
    wrist = hand_landmarks.landmark[0]
    h, w, _ = img.shape
    cx = int(wrist.x * w)
    cy = int(wrist.y * h)
    return cx, cy 

while True:
    success, img = cap.read()
    if not success:
        break

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            cx, cy = extract_hands_coordinates(hand_landmarks)
            if prev_x is not None and abs(prev_x - cx) > threshold_x:
                if cx < prev_x:
                    trigger_command(COMMANDS.RIGHT)
                elif cx > prev_x:
                    trigger_command(COMMANDS.LEFT)
            elif prev_y is not None and abs(prev_y - cy) > threshold_y:
                if cy < prev_y:
                    trigger_command(COMMANDS.UP)
                elif cy > prev_y:
                    trigger_command(COMMANDS.DOWN) 
               
            prev_x = cx
            prev_y = cy           

    cv2.imshow("Hand Tracking", img)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()

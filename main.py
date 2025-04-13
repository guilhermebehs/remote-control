import cv2
import mediapipe as mp
from commands_adapter import CommandsAdapter

commandsAdapter = CommandsAdapter()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

prev_x = None
direction = ''

while True:
    success, img = cap.read()
    if not success:
        break

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get wrist landmark (ID 0)
            wrist = hand_landmarks.landmark[0]
            h, w, _ = img.shape
            cx = int(wrist.x * w)  # Convert normalized to pixel position

            # Compare to previous frame
           
            if prev_x is not None and abs(prev_x - cx) > 50:
                if cx < prev_x:
                  #commandsAdapter.right()
                  print("right")
                elif cx > prev_x:    
                #commandsAdapter.left()
                  print("left")

            
            prev_x = cx

    cv2.imshow("Hand Tracking", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
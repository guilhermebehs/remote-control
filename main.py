import threading
import cv2
import mediapipe as mp
import time
from commands_adapter import CommandsAdapter

commandsAdapter = CommandsAdapter()


def is_hand_closed(hand_landmarks):
    # Landmarks for finger tips and pip joints
    tips_ids = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky tips
    pip_ids = [6, 10, 14, 18]   # Corresponding PIP joints

    closed_fingers = 0

    for tip_id, pip_id in zip(tips_ids, pip_ids):
        tip = hand_landmarks.landmark[tip_id]
        pip = hand_landmarks.landmark[pip_id]

        if tip.y > pip.y:  # Remember: lower y means higher on screen
            closed_fingers += 1

    return closed_fingers >= 4  # You can tweak this threshold


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

prev_x = None
prev_y = None
prev_hands_close = None

threshold_x = 100
threshold_y = 100

cooldown = {
    commandsAdapter.left: 1.0,
    commandsAdapter.right: 1.0,
    commandsAdapter.up: 1.0,
    commandsAdapter.down: 1.0,
    commandsAdapter.enter: 2.0,
}
last_trigger_times = {
    commandsAdapter.left: 0,
    commandsAdapter.right: 0,
    commandsAdapter.up: 0,
    commandsAdapter.down: 0,
    commandsAdapter.enter: 0,

}

def trigger_command(func):
    now = time.time()
    if now - last_trigger_times[func] >= cooldown[func]:
        last_trigger_times[func] = now
        threading.Thread(target=func).start()
      
while True:
    success, img = cap.read()
    if not success:
        break

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            wrist = hand_landmarks.landmark[0]
            h, w, _ = img.shape
            cx = int(wrist.x * w)
            cy = int(wrist.y * h)
            
            hands_closed = is_hand_closed(hand_landmarks) 
            if prev_hands_close is not None and prev_hands_close != hands_closed :
               if hands_closed:
                 trigger_command(commandsAdapter.enter)

            elif prev_x is not None and abs(prev_x - cx) > threshold_x:
                if cx < prev_x:
                    trigger_command(commandsAdapter.right)
                elif cx > prev_x:
                    trigger_command(commandsAdapter.left)

            elif prev_y is not None and abs(prev_y - cy) > threshold_y:
                if cy < prev_y:
                    trigger_command(commandsAdapter.up)
                elif cy > prev_y:
                    trigger_command(commandsAdapter.down)        

            prev_x = cx
            prev_y = cy
            prev_hands_close = hands_closed


    cv2.imshow("Hand Tracking", img)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()

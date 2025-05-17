import threading
import cv2
import mediapipe as mp
import time
from commands_adapter import CommandsAdapter
import speech_recognition as sr
import threading

commandsAdapter = CommandsAdapter()


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
    commandsAdapter.back: 2.0,
}
last_trigger_times = {
    commandsAdapter.left: 0,
    commandsAdapter.right: 0,
    commandsAdapter.up: 0,
    commandsAdapter.down: 0,
    commandsAdapter.enter: 0,
    commandsAdapter.back: 0,
    

}

def trigger_command(func):
    now = time.time()
    if now - last_trigger_times[func] >= cooldown[func]:
        last_trigger_times[func] = now
        threading.Thread(target=func).start()
      


def recognize_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    while True:
        with mic as source:
            try:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio,language="pt-BR")
                if command == "selecionar":
                    trigger_command(commandsAdapter.enter)
                elif command == "voltar":
                    trigger_command(commandsAdapter.back)    
            except sr.UnknownValueError:
                print("Could not understand audio.")
            except sr.RequestError as e:
                print(f"API unavailable or error: {e}")
            except sr.WaitTimeoutError:
                print("Listening timed out while waiting for phrase.")
            except KeyboardInterrupt:
                print("Stopping recognition thread.")
                

# Create and start thread
thread = threading.Thread(target=recognize_speech)
thread.start()


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
            
            
            if prev_x is not None and abs(prev_x - cx) > threshold_x:
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


    cv2.imshow("Hand Tracking", img)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()

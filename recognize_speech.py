from trigger_command import trigger_command
from commands_enum import COMMANDS
import speech_recognition as sr

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
                    trigger_command(COMMANDS.ENTER)
                elif command == "voltar":
                    trigger_command(COMMANDS.BACK)       
            except sr.UnknownValueError:
                print("Could not understand audio.")
            except sr.RequestError as e:
                print(f"API unavailable or error: {e}")
            except sr.WaitTimeoutError:
                print("Listening timed out while waiting for phrase.")
            except KeyboardInterrupt:
                print("Stopping recognition thread.")
